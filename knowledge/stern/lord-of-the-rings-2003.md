# Lord of the Rings

Coverage: **partial - source-derived recreation knowledge requiring validation**

## Overview

Legacy evidence identifies this candidate as Stern (2003). The information below is preserved for recreation work but is not automatically treated as validated physical-machine fact.

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

- `games/lotr.json#/switches/0._note`: Controller.Switch on/off. Ball enters VUK, kicked out by SolLVUK (coil 3).
- `games/lotr.json#/switches/1._note`: PulseSw 10. Drop target or standup target.
- `games/lotr.json#/switches/2._note`: Manual trough. sw11 is deepest position (nearest drain). Controller.Switch on/off with UpdateTrough.
- `games/lotr.json#/switches/5._note`: Manual trough. sw14 is nearest shooter lane — ball ejected from here by SolRelease (coil 1).
- `games/lotr.json#/switches/6._note`: PulseSw 15 fired in SolRelease after trough eject. Confirms ball reached shooter lane.
- `games/lotr.json#/switches/7._note`: Controller.Switch on/off. Also plungerIM.switch 16 — impulse plunger lane switch.
- `games/lotr.json#/switches/8._note`: Controller.Switch on/off. Ball lock position on sword ramp.
- `games/lotr.json#/switches/9._note`: Controller.Switch on/off. Second ball lock position on sword ramp.
- `games/lotr.json#/switches/10._note`: Controller.Switch on/off. Top lock position. Triggers sword glow (Lampz 101) when occupied.
- `games/lotr.json#/switches/11._note`: Controller.Switch on/off
- `games/lotr.json#/switches/12._note`: Controller.Switch on/off
- `games/lotr.json#/switches/13._note`: Controller.Switch on/off
- `games/lotr.json#/switches/14._note`: PulseSw 23. Animated standup target with gate model (g01_sw23).
- `games/lotr.json#/switches/15._note`: Controller.Switch on/off. Triggers WireRampOff on hit, WireRampOn on unhit.
- `games/lotr.json#/switches/16._note`: Controller.Switch on/off. Direction-aware — checks activeball.vely for WireRampOn direction.
- `games/lotr.json#/switches/17._note`: Controller.Switch set on BalrogFlipper_Collide when Balrog is closed and hit force > 3. Cleared after wobble settles. Not a VPX trigger — mechanical collision detection.
- `games/lotr.json#/switches/18._note`: PulseSw 29. Animated standup target with gate model (g01_sw29).
- `games/lotr.json#/switches/19._note`: Controller.Switch on/off. Ball enters right VUK, kicked out by SolRVUK (coil 5).
- `games/lotr.json#/switches/20._note`: Controller.Switch set by SolBalrog when Balrog opens (BalrogDir toggling). Mechanism position switch.
- `games/lotr.json#/switches/21._note`: Controller.Switch set by SolBalrog when Balrog closes (BalrogDir toggling). Mechanism position switch.
- `games/lotr.json#/switches/22._note`: Controller.Switch on/off
- `games/lotr.json#/switches/23._note`: Controller.Switch on/off
- `games/lotr.json#/switches/24._note`: Controller.Switch on/off
- `games/lotr.json#/switches/25._note`: Controller.Switch on/off
- `games/lotr.json#/switches/26._note`: Controller.Switch on/off
- `games/lotr.json#/switches/27._note`: Controller.Switch on/off
- `games/lotr.json#/switches/28._note`: Controller.Switch on/off
- `games/lotr.json#/switches/29._note`: Controller.Switch on/off
- `games/lotr.json#/switches/30._note`: Controller.Switch on/off. Ball enters VUK, kicked out by SolULVUK (coil 4). Triggers POTD lamp (Lampz 100).
- `games/lotr.json#/switches/31._note`: Controller.Switch on/off
- `games/lotr.json#/switches/32._note`: Controller.Switch on/off
- `games/lotr.json#/switches/33._note`: Controller.Switch on/off
- `games/lotr.json#/switches/34._note`: Controller.Switch on/off
- `games/lotr.json#/switches/35._note`: Controller.Switch on/off. Ball caught in saucer, kicked out by SolURKicker (coil 19).
- `games/lotr.json#/switches/36._note`: Controller.Switch on/off. Ball in ring magnet area. Has stuck-ball timer. Separate VPX magnet object sw47a with cvpmMagnet.
- `games/lotr.json#/switches/37._note`: Controller.Switch on/off. Triggers WireRampOn on hit. Nudges ball VelX on unhit.
- `games/lotr.json#/switches/38._note`: PulseSw 49
- `games/lotr.json#/switches/39._note`: PulseSw 50
- `games/lotr.json#/switches/40._note`: PulseSw 51
- `games/lotr.json#/switches/41._note`: PulseSw 52 from sw52_Spin sub.
- `games/lotr.json#/switches/42._note`: PulseSw 53. Triggers EyeLookAt. Near Palantir eye.
- `games/lotr.json#/switches/43._note`: vpmNudge.TiltSwitch = 56
- `games/lotr.json#/switches/44._note`: Controller.Switch on/off. Triggers EyeLookAt.
- `games/lotr.json#/switches/45._note`: Controller.Switch on/off. Triggers EyeLookAt.
- `games/lotr.json#/switches/46._note`: PulseSw 59 in LeftSlingShot_Slingshot sub
- `games/lotr.json#/switches/47._note`: Controller.Switch on/off. Triggers EyeLookAt.
- `games/lotr.json#/switches/48._note`: Controller.Switch on/off. Triggers EyeLookAt.
- `games/lotr.json#/switches/49._note`: PulseSw 62 in RightSlingShot_Slingshot sub
- `games/lotr.json#/coils/0._vbscript_callback`: SolRelease
- `games/lotr.json#/coils/0._inferred_type`: ball_management
- `games/lotr.json#/coils/0._note`: Kicks from sw14, PulseSw 15 (shooter lane confirm)
- `games/lotr.json#/coils/1._vbscript_callback`: AutoPlunger
- `games/lotr.json#/coils/1._inferred_type`: ball_management
- `games/lotr.json#/coils/1._note`: Impulse plunger. plungerIM.AutoFire. VPX object: swPlunger.
- `games/lotr.json#/coils/2._vbscript_callback`: SolLVUK
- `games/lotr.json#/coils/2._inferred_type`: ball_management
- `games/lotr.json#/coils/2._note`: Kicks ball from sw9 VUK upward. KickBall with z-lift.
- `games/lotr.json#/coils/3._vbscript_callback`: SolULVUK
- `games/lotr.json#/coils/3._inferred_type`: ball_management
- `games/lotr.json#/coils/3._note`: Kicks ball from sw41 VUK. KickBall with z-lift 230.
- `games/lotr.json#/coils/4._vbscript_callback`: SolRVUK
- `games/lotr.json#/coils/4._inferred_type`: ball_management
- `games/lotr.json#/coils/4._note`: Kicks ball from sw30 right VUK upward.
- `games/lotr.json#/coils/5._vbscript_callback`: SolRingMag
- `games/lotr.json#/coils/5._inferred_type`: mechanism
- `games/lotr.json#/coils/5._note`: cvpmMagnet. GrabCenter=True. Controls ring magnet on/off. Kicks ball out when disabled.
- `games/lotr.json#/coils/6._vbscript_callback`: SolTower
- `games/lotr.json#/coils/6._inferred_type`: mechanism
- `games/lotr.json#/coils/6._note`: Animates Orthanc/Barad-dur tower raising and lowering via TowerAnim timer. 20-step animation.
- `games/lotr.json#/coils/7._vbscript_callback`: SolDiv
- `games/lotr.json#/coils/7._inferred_type`: diverter
- `games/lotr.json#/coils/7._note`: Rotates DiverterFlipper to end/start. Controls ball path on playfield.
- `games/lotr.json#/coils/8._inferred_type`: mechanism
- `games/lotr.json#/coils/8._note`: Bumper solenoid. Handled by VPM framework (core.vbs), not table SolCallback. Comment in script: '9 left bumper'.
- `games/lotr.json#/coils/9._inferred_type`: mechanism
- `games/lotr.json#/coils/9._note`: Bumper solenoid. Handled by VPM framework (core.vbs). Comment: '10 right bumper'.
- `games/lotr.json#/coils/10._inferred_type`: mechanism
- `games/lotr.json#/coils/10._note`: Bumper solenoid. Handled by VPM framework (core.vbs). Comment: '11 bottom bumper'.
- `games/lotr.json#/coils/11._vbscript_callback`: SolOrbit
- `games/lotr.json#/coils/11._inferred_type`: gate
- `games/lotr.json#/coils/11._note`: OrbitPin.IsDropped toggled by Enabled state. Controls orbit one-way gate.
- `games/lotr.json#/coils/12._vbscript_callback`: Flash14
- `games/lotr.json#/coils/12._inferred_type`: flasher
- `games/lotr.json#/coils/12._note`: Non-ModSol: Flash14 sub. ModSol: ModLampz.SetModLamp 14. PWM SolMask(1014).
- `games/lotr.json#/coils/13._inferred_type`: flipper
- `games/lotr.json#/coils/13._note`: Flipper solenoid. Handled by VPM framework (core.vbs). Comment: '15 left flipper'. Not same as sLLFlipper constant (which is 48).
- `games/lotr.json#/coils/14._inferred_type`: flipper
- `games/lotr.json#/coils/14._note`: Flipper solenoid. Handled by VPM framework (core.vbs). Comment: '16 right flipper'. Not same as sLRFlipper constant (which is 46).
- `games/lotr.json#/coils/15._inferred_type`: mechanism
- `games/lotr.json#/coils/15._note`: Slingshot solenoid. Handled by VPM framework (core.vbs). Comment: '17 left slingshot'.
- `games/lotr.json#/coils/16._inferred_type`: mechanism
- `games/lotr.json#/coils/16._note`: Slingshot solenoid. Handled by VPM framework (core.vbs). Comment: '18 right slingshot'.
- `games/lotr.json#/coils/17._vbscript_callback`: SolURKicker
- `games/lotr.json#/coils/17._inferred_type`: ball_management
- `games/lotr.json#/coils/17._note`: Kicks ball from sw46 saucer at angle 270.
- `games/lotr.json#/coils/18._inferred_type`: mechanism
- `games/lotr.json#/coils/18._note`: Comment: '20 balrog motor relay'. No SolCallback — motor relay likely handled by VPM or used for power relay only.
- `games/lotr.json#/coils/19._vbscript_callback`: SolLockRelease
- `games/lotr.json#/coils/19._inferred_type`: mechanism
- `games/lotr.json#/coils/19._note`: Drops Lockpin to release locked balls from sword ramp. Timed re-raise after 280ms.
- `games/lotr.json#/coils/20._vbscript_callback`: SolBalrog
- `games/lotr.json#/coils/20._inferred_type`: mechanism
- `games/lotr.json#/coils/20._note`: Toggles Balrog figure open/close. Sets switches 31 (opening) and 32 (closed) as position feedback. Animated via BalrogOpen/BalrogClose timers.
- `games/lotr.json#/coils/21._vbscript_callback`: Flash23
- `games/lotr.json#/coils/21._inferred_type`: flasher
- `games/lotr.json#/coils/21._note`: Non-ModSol: Flash23 sub. ModSol: ModLampz.SetModLamp 23. PWM SolMask(1023).
- `games/lotr.json#/coils/22._vbscript_callback`: SolKnocker
- `games/lotr.json#/coils/22._inferred_type`: knocker
- `games/lotr.json#/coils/23._vbscript_callback`: Flash25
- `games/lotr.json#/coils/23._inferred_type`: flasher
- `games/lotr.json#/coils/23._note`: Non-ModSol: Flash25 sub. ModSol: ModLampz.SetModLamp 25. PWM SolMask(1025).
- `games/lotr.json#/coils/24._vbscript_callback`: Flash26
- `games/lotr.json#/coils/24._inferred_type`: flasher
- `games/lotr.json#/coils/24._note`: Non-ModSol: Flash26 sub. ModSol: ModLampz.SetModLamp 26. PWM SolMask(1026).
- `games/lotr.json#/coils/25._vbscript_callback`: Flash27
- `games/lotr.json#/coils/25._inferred_type`: flasher
- `games/lotr.json#/coils/25._note`: Non-ModSol: Flash27 sub. ModSol: ModLampz.SetModLamp 27. PWM SolMask(1027).
- `games/lotr.json#/coils/26._vbscript_callback`: Flash29
- `games/lotr.json#/coils/26._inferred_type`: flasher
- `games/lotr.json#/coils/26._note`: Non-ModSol: Flash29 sub. ModSol: ModLampz.SetModLamp 29. PWM SolMask(1029).
- `games/lotr.json#/coils/27._vbscript_callback`: Lampz.SetLamp 130,
- `games/lotr.json#/coils/27._inferred_type`: flasher
- `games/lotr.json#/coils/27._note`: Non-ModSol: Lampz.SetLamp 130. ModSol: ModLampz.SetModLamp 30. PWM SolMask(1030). VPX objects: f130, f130l.
- `games/lotr.json#/coils/28._vbscript_callback`: Lampz.SetLamp 131,
- `games/lotr.json#/coils/28._inferred_type`: flasher
- `games/lotr.json#/coils/28._note`: Non-ModSol: Lampz.SetLamp 131. ModSol: ModLampz.SetModLamp 31. PWM SolMask(1031). ModLampz callback: DisableLighting p19 (DTR insert).
- `games/lotr.json#/coils/29._vbscript_callback`: Lampz.SetLamp 132,
- `games/lotr.json#/coils/29._inferred_type`: flasher
- `games/lotr.json#/coils/29._note`: Non-ModSol: Lampz.SetLamp 132. ModSol: ModLampz.SetModLamp 32. PWM SolMask(1032). ModLampz callback: ModFlash32 (BalrogImageSwap). VPX object: Lbalrogbloom.
- `games/lotr.json#/lamps/72._note`: MassAssign commented out. Callback DisableLighting p73 still active.
- `games/lotr.json#/lamps/73._note`: MassAssign commented out. Callback DisableLighting p74 still active.
- `games/lotr.json#/lamps/74._note`: MassAssign commented out. Callback DisableLighting p75 still active.
- `games/lotr.json#/lamps/75._note`: MassAssign commented out. Callback DisableLighting p76 still active.
- `games/lotr.json#/lamps/76._note`: MassAssign commented out. Callback DisableLighting p77 still active.
- `games/lotr.json#/lamps/77._note`: MassAssign commented out. Callback DisableLighting p78 still active.
- `games/lotr.json#/lamps/97._note`: Special lamp. 5 VPX objects: l_potd_1 through l_potd_5. Slow fade speed.
- `games/lotr.json#/lamps/98._note`: Special lamp. Triggered by sw19 (lock 3). VPX objects: swordflash, swordflashs. Slow fade.
- `games/lotr.json#/lamps/99._note`: Special lamp. VPX objects: Lvial, Lvialhalo. Very slow fade.
- `games/lotr.json#/_source/confidence_notes`: High confidence on switches and coils. No Const sw* definitions — switches identified from _Hit/_UnHit subs, Controller.Switch() calls, and PulseSw calls. Manual trough (not cvpmTrough) with 4 kicker switches (sw11-sw14) and PulseSw 15 for shooter lane confirm. Lamp IDs from Lampz.MassAssign/Callback (IDs 1-99 matrix lamps, 100-102 special lamps, 130-132 flasher lamps). Flashers (coils 14, 23, 25-27, 29-32) use Flash subs or Lampz.SetLamp with 100+ IDs, plus ModLampz for PWM mode. Balrog mechanism uses switches 28, 31, 32 and solenoid 22. Ring magnet (sol 6) with sw47. Tower mechanism (sol 7). SEGA.VBS = Whitestar platform. Solenoids 9-11 (bumpers), 15-16 (flippers), 17-18 (slingshots) handled by core.vbs framework — not in table script SolCallbacks.

## Unresolved questions

- Is the I/O enumeration complete for every supported physical/controller variant?
- Which inferred VPX behaviors reflect real hardware, and which are table-script conveniences?
- Are all mechanism home states, sensors, motion constraints, and ball interactions documented?

## Sources

- `legacy.game.lotr`: `games/lotr.json` at the pinned migration revision.
