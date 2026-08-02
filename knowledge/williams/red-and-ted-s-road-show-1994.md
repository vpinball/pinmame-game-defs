# Red and Ted's Road Show

Coverage: **partial - source-derived recreation knowledge requiring validation**

## Overview

Legacy evidence identifies this candidate as Williams (1994). The information below is preserved for recreation work but is not automatically treated as validated physical-machine fact.

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
- `games/rs.json#/switches/0._inferred_type`: target
- `games/rs.json#/switches/0._note`: PulseSw 11 via sw11_Hit. Ted's mouth opto — ball enters Ted's mouth when jaw is open.
- `games/rs.json#/switches/1._inferred_type`: opto
- `games/rs.json#/switches/1._note`: Bulldozer mechanism position switch (down). Managed by cvpmMech BulldozerMech .AddSw 12, 0, 0.
- `games/rs.json#/switches/2._inferred_type`: cabinet
- `games/rs.json#/switches/3._inferred_type`: tilt
- `games/rs.json#/switches/3._note`: vpmNudge.TiltSwitch = 14
- `games/rs.json#/switches/4._inferred_type`: opto
- `games/rs.json#/switches/4._note`: Bulldozer mechanism position switch (up). Managed by cvpmMech BulldozerMech .AddSw 15, 10, 11.
- `games/rs.json#/switches/5._inferred_type`: rollover
- `games/rs.json#/switches/6._inferred_type`: rollover
- `games/rs.json#/switches/7._inferred_type`: rollover
- `games/rs.json#/switches/8._inferred_type`: tilt
- `games/rs.json#/switches/9._inferred_type`: cabinet
- `games/rs.json#/switches/9._note`: Controller.Switch(22) = 1 on init
- `games/rs.json#/switches/10._inferred_type`: cabinet
- `games/rs.json#/switches/10._note`: Controller.Switch(23) toggled via KeyFront
- `games/rs.json#/switches/11._inferred_type`: cabinet
- `games/rs.json#/switches/11._note`: Controller.Switch(24) = 1 on init. Comment: 'and keep it close'. WPC column 3 always-closed switch.
- `games/rs.json#/switches/12._inferred_type`: saucer
- `games/rs.json#/switches/12._note`: Red's mouth saucer. bsRed.AddBall on hit. Eject via coil 24 (bsRed.SolOut).
- `games/rs.json#/switches/13._inferred_type`: rollover
- `games/rs.json#/switches/14._inferred_type`: rollover
- `games/rs.json#/switches/15._inferred_type`: target
- `games/rs.json#/switches/15._note`: 3 targets (T28a, T28b, T28c) all pulse switch 28.
- `games/rs.json#/switches/16._inferred_type`: rollover
- `games/rs.json#/switches/17._inferred_type`: rollover
- `games/rs.json#/switches/18._inferred_type`: rollover
- `games/rs.json#/switches/19._inferred_type`: target
- `games/rs.json#/switches/19._note`: 3 targets (T34a, T34b, T34c) all pulse switch 34.
- `games/rs.json#/switches/20._inferred_type`: target
- `games/rs.json#/switches/21._inferred_type`: target
- `games/rs.json#/switches/22._inferred_type`: target
- `games/rs.json#/switches/22._note`: PulseSw 37 via sw37a_Hit. Red's jaw target. sw37_Hit plays sound only (mouth plastic hit).
- `games/rs.json#/switches/23._inferred_type`: rollover
- `games/rs.json#/switches/24._inferred_type`: trough
- `games/rs.json#/switches/24._note`: PulseSw 41 called in SolRelease (coil 1 callback). Trough jam/ball-near-shooter detection.
- `games/rs.json#/switches/25._inferred_type`: trough
- `games/rs.json#/switches/25._note`: First trough switch (closest to shooter). Custom trough implementation with UpdateTrough timer. Ball created at init: sw42.CreateSizedballWithMass.
- `games/rs.json#/switches/26._inferred_type`: trough
- `games/rs.json#/switches/27._inferred_type`: trough
- `games/rs.json#/switches/28._inferred_type`: trough
- `games/rs.json#/switches/28._note`: Last trough switch (furthest from shooter). 4-ball trough.
- `games/rs.json#/switches/29._inferred_type`: rollover
- `games/rs.json#/switches/30._inferred_type`: target
- `games/rs.json#/switches/30._note`: PulseSw 47. Bulldozer proximity sensor — detects ball hitting bulldozer blade.
- `games/rs.json#/switches/31._inferred_type`: target
- `games/rs.json#/switches/31._note`: PulseSw 48. Ted's mouth plastic — ball hitting Ted's jaw.
- `games/rs.json#/switches/32._inferred_type`: spinner
- `games/rs.json#/switches/32._note`: sw51spinner_Spin event pulses switch 51.
- `games/rs.json#/switches/33._inferred_type`: rollover
- `games/rs.json#/switches/33._note`: First lock switch in Bob's Bunker lock lane.
- `games/rs.json#/switches/34._inferred_type`: rollover
- `games/rs.json#/switches/34._note`: Second lock switch in Bob's Bunker lock lane.
- `games/rs.json#/switches/35._inferred_type`: saucer
- `games/rs.json#/switches/35._note`: Lock kickout position. KickerBall54 stores activeball reference for coil 8 (SolLockKickOut) ejection.
- `games/rs.json#/switches/36._inferred_type`: rollover
- `games/rs.json#/switches/36._note`: Right ramp exit to left mini flipper area.
- `games/rs.json#/switches/37._inferred_type`: rollover
- `games/rs.json#/switches/38._inferred_type`: rollover
- `games/rs.json#/switches/39._inferred_type`: rollover
- `games/rs.json#/switches/39._note`: Left plunger lane. On hit: PPL=True, switches MechPlunger to left plunger. Flying Rocks skill shot lane.
- `games/rs.json#/switches/40._inferred_type`: slingshot
- `games/rs.json#/switches/40._note`: LeftSlingShot_Slingshot event pulses switch 61.
- `games/rs.json#/switches/41._inferred_type`: slingshot
- `games/rs.json#/switches/41._note`: RightSlingShot_Slingshot event pulses switch 62.
- `games/rs.json#/switches/42._inferred_type`: bumper
- `games/rs.json#/switches/42._note`: Bumper3_hit pulses switch 63.
- `games/rs.json#/switches/43._inferred_type`: bumper
- `games/rs.json#/switches/43._note`: Bumper1_hit pulses switch 64.
- `games/rs.json#/switches/44._inferred_type`: bumper
- `games/rs.json#/switches/44._note`: Bumper2_hit pulses switch 65.
- `games/rs.json#/switches/45._inferred_type`: rollover
- `games/rs.json#/switches/46._inferred_type`: rollover
- `games/rs.json#/switches/46._note`: Right ramp center exit (habitrail back to right inlane).
- `games/rs.json#/switches/47._inferred_type`: rollover
- `games/rs.json#/switches/47._note`: Flying rocks lane — awards 5X Blast.
- `games/rs.json#/switches/48._inferred_type`: rollover
- `games/rs.json#/switches/48._note`: Flying rocks lane — awards Radio Riot.
- `games/rs.json#/switches/49._inferred_type`: rollover
- `games/rs.json#/switches/49._note`: Flying rocks lane — awards Extra Ball.
- `games/rs.json#/switches/50._inferred_type`: rollover
- `games/rs.json#/switches/51._inferred_type`: saucer
- `games/rs.json#/switches/51._note`: Blast Zone / Skill Shot hole. Feeds to Start City.
- `games/rs.json#/switches/52._inferred_type`: saucer
- `games/rs.json#/switches/52._note`: Start City scoop/hole. Eject via coil 6 (StartCitySolOut). Controller.Switch(78) on/off directly.
- `games/rs.json#/switches/53._inferred_type`: target
- `games/rs.json#/switches/53._note`: PulseSw 81. Cone zone target.
- `games/rs.json#/switches/54._inferred_type`: target
- `games/rs.json#/switches/54._note`: PulseSw 82. Cone zone target. T82P rotates on hit.
- `games/rs.json#/switches/55._inferred_type`: target
- `games/rs.json#/switches/55._note`: PulseSw 83. Cone zone target.
- `games/rs.json#/switches/56._inferred_type`: target
- `games/rs.json#/switches/56._note`: PulseSw 84. Cone zone target.
- `games/rs.json#/switches/57._inferred_type`: rollover
- `games/rs.json#/switches/58._inferred_type`: rollover
- `games/rs.json#/coils/0._vbscript_callback`: SolRelease
- `games/rs.json#/coils/0._inferred_type`: ball_management
- `games/rs.json#/coils/0._note`: Kicks ball from trough (sw42) to shooter lane. Also pulses sw41 (trough jam).
- `games/rs.json#/coils/1._vbscript_callback`: LowerLeftDiverter
- `games/rs.json#/coils/1._inferred_type`: diverter
- `games/rs.json#/coils/1._note`: Controls diverter1/diverter2 VPX flipper objects. Routes ball to left shooter lane (Flying Rocks).
- `games/rs.json#/coils/2._vbscript_callback`: LockupPin
- `games/rs.json#/coils/2._inferred_type`: mechanism
- `games/rs.json#/coils/2._note`: Controls sol3lockup wall. When enabled, drops wall to release locked balls.
- `games/rs.json#/coils/3._vbscript_callback`: UpperLeftDiverter
- `games/rs.json#/coils/3._inferred_type`: diverter
- `games/rs.json#/coils/3._note`: Left ramp diverter. Routes ball left vs right on left ramp exit.
- `games/rs.json#/coils/4._vbscript_callback`: UpperRightDiverter
- `games/rs.json#/coils/4._inferred_type`: diverter
- `games/rs.json#/coils/4._note`: Right ramp diverter. Routes ball to center habitrail vs mini flipper area.
- `games/rs.json#/coils/5._vbscript_callback`: StartCitySolOut
- `games/rs.json#/coils/5._inferred_type`: kicker
- `games/rs.json#/coils/5._note`: Ejects ball from Start City scoop (sw78). sw78.KickZ with randomized force.
- `games/rs.json#/coils/6._vbscript_callback`: vpmSolSound SoundFX("Knocker",DOFKnocker),
- `games/rs.json#/coils/6._inferred_type`: knocker
- `games/rs.json#/coils/7._vbscript_callback`: SolLockKickOut
- `games/rs.json#/coils/7._inferred_type`: kicker
- `games/rs.json#/coils/7._note`: Ejects ball from lock position (sw54) via KickBall function.
- `games/rs.json#/coils/8._vbscript_callback`: TedEyesLeft
- `games/rs.json#/coils/8._inferred_type`: mechanism
- `games/rs.json#/coils/8._note`: Animates Ted's eyes to look left. Talking head mechanism.
- `games/rs.json#/coils/9._vbscript_callback`: TedLidsDown
- `games/rs.json#/coils/9._inferred_type`: mechanism
- `games/rs.json#/coils/9._note`: Closes Ted's eyelids. Talking head mechanism.
- `games/rs.json#/coils/10._vbscript_callback`: TedLidsUp
- `games/rs.json#/coils/10._inferred_type`: mechanism
- `games/rs.json#/coils/10._note`: Opens Ted's eyelids. Talking head mechanism.
- `games/rs.json#/coils/11._vbscript_callback`: TedEyesRight
- `games/rs.json#/coils/11._inferred_type`: mechanism
- `games/rs.json#/coils/11._note`: Animates Ted's eyes to look right. Talking head mechanism.
- `games/rs.json#/coils/12._vbscript_callback`: RedLidsDown
- `games/rs.json#/coils/12._inferred_type`: mechanism
- `games/rs.json#/coils/12._note`: Closes Red's eyelids. Talking head mechanism.
- `games/rs.json#/coils/13._vbscript_callback`: RedEyesLeft
- `games/rs.json#/coils/13._inferred_type`: mechanism
- `games/rs.json#/coils/13._note`: Animates Red's eyes to look left. Talking head mechanism.
- `games/rs.json#/coils/14._vbscript_callback`: RedLidsUp
- `games/rs.json#/coils/14._inferred_type`: mechanism
- `games/rs.json#/coils/14._note`: Opens Red's eyelids. Talking head mechanism.
- `games/rs.json#/coils/15._vbscript_callback`: RedEyesRight
- `games/rs.json#/coils/15._inferred_type`: mechanism
- `games/rs.json#/coils/15._note`: Animates Red's eyes to look right. Talking head mechanism.
- `games/rs.json#/coils/16._vbscript_callback`: RedMotorOn
- `games/rs.json#/coils/16._inferred_type`: mechanism
- `games/rs.json#/coils/16._note`: Red's jaw motor. cvpmMech RedJawMech Sol1=17. Talking head mechanism.
- `games/rs.json#/coils/17._inferred_type`: mechanism
- `games/rs.json#/coils/17._note`: Red's jaw motor direction. cvpmMech RedJawMech Sol2=18. SolCallback commented out — handled by cvpmMech internally.
- `games/rs.json#/coils/18._inferred_type`: mechanism
- `games/rs.json#/coils/18._note`: Ted's jaw motor direction. cvpmMech TedJawMech Sol2=19. SolCallback commented out — handled by cvpmMech internally.
- `games/rs.json#/coils/19._vbscript_callback`: TedMotorOn
- `games/rs.json#/coils/19._inferred_type`: mechanism
- `games/rs.json#/coils/19._note`: Ted's jaw motor. cvpmMech TedJawMech Sol1=20. Talking head mechanism.
- `games/rs.json#/coils/20._vbscript_callback`: BullDozerMotor
- `games/rs.json#/coils/20._inferred_type`: mechanism
- `games/rs.json#/coils/20._note`: Bulldozer motor. cvpmMech BulldozerMech Sol1=23. Steps=11, switches at positions 12 (down) and 15 (up).
- `games/rs.json#/coils/21._vbscript_callback`: bsRed.SolOut
- `games/rs.json#/coils/21._inferred_type`: kicker
- `games/rs.json#/coils/21._note`: Ejects ball from Red's mouth saucer (sw25).
- `games/rs.json#/coils/22._vbscript_callback`: ShakerMotorSol
- `games/rs.json#/coils/22._inferred_type`: mechanism
- `games/rs.json#/coils/22._note`: Shaker motor for physical feedback. Configurable intensity (0-3) and volume.
- `games/rs.json#/coils/23._vbscript_callback`: FlashSolMod51
- `games/rs.json#/coils/23._inferred_type`: flasher
- `games/rs.json#/coils/23._note`: WPC aux board flasher. SolModCallBack(51). Flasher 9 (white) in InitAllFlashers.
- `games/rs.json#/coils/24._vbscript_callback`: FlashSolMod52
- `games/rs.json#/coils/24._inferred_type`: flasher
- `games/rs.json#/coils/24._note`: WPC aux board flasher. SolModCallBack(52). Flasher 7 (yellow) in InitAllFlashers.
- `games/rs.json#/coils/25._vbscript_callback`: FlashSolMod53
- `games/rs.json#/coils/25._inferred_type`: flasher
- `games/rs.json#/coils/25._note`: WPC aux board flasher. SolModCallBack(53). Flashers 1+2 (white) in InitAllFlashers.
- `games/rs.json#/coils/26._vbscript_callback`: FlashSolMod54
- `games/rs.json#/coils/26._inferred_type`: flasher
- `games/rs.json#/coils/26._note`: WPC aux board flasher. SolModCallBack(54). Flashers 3+4 (yellow) in InitAllFlashers.
- `games/rs.json#/coils/27._vbscript_callback`: FlashSolMod55
- `games/rs.json#/coils/27._inferred_type`: flasher
- `games/rs.json#/coils/27._note`: WPC aux board flasher. SolModCallBack(55). Flashers 5+6 (red) in InitAllFlashers.
- `games/rs.json#/coils/28._vbscript_callback`: FlashSolMod56
- `games/rs.json#/coils/28._inferred_type`: flasher
- `games/rs.json#/coils/28._note`: WPC aux board flasher. SolModCallBack(56). Flasher 11 (white) in InitAllFlashers.
- `games/rs.json#/coils/29._vbscript_callback`: FlashSolMod57
- `games/rs.json#/coils/29._inferred_type`: flasher
- `games/rs.json#/coils/29._note`: WPC aux board flasher. SolModCallBack(57). Flasher 8 (white) in InitAllFlashers.
- `games/rs.json#/coils/30._vbscript_callback`: FlashSolMod58
- `games/rs.json#/coils/30._inferred_type`: flasher
- `games/rs.json#/coils/30._note`: WPC aux board flasher. SolModCallBack(58). Flasher 10 (orange) in InitAllFlashers.
- `games/rs.json#/coils/31._vbscript_callback`: SolRFlipper
- `games/rs.json#/coils/31._inferred_type`: flipper
- `games/rs.json#/coils/31._note`: Framework constant sLRFlipper=46. SolCallback(sLRFlipper).
- `games/rs.json#/coils/32._vbscript_callback`: SolLFlipper
- `games/rs.json#/coils/32._inferred_type`: flipper
- `games/rs.json#/coils/32._note`: Framework constant sLLFlipper=48. SolCallback(sLLFlipper). Main lower left flipper.
- `games/rs.json#/coils/33._vbscript_callback`: SolUFlipper
- `games/rs.json#/coils/33._inferred_type`: flipper
- `games/rs.json#/coils/33._note`: Framework constant sULFlipper (value not in table script — defined in wpc.VBS). Controls LeftFlipper1 and LeftFlipper2 simultaneously. SolCallback(sULFlipper).
- `games/rs.json#/lamps/26._note`: Lampz.Callback(43) reassigned to bc43 (radio toy lamp).
- `games/rs.json#/lamps/54._note`: Lampz.Callback(77) uses bc77. Bulb above playfield, no standard light object.
- `games/rs.json#/lamps/56._note`: Lampz.Callback(81) uses bc81. Bulb above playfield.
- `games/rs.json#/lamps/57._note`: Lampz.Callback(82) uses bc82. Bulb above playfield.
- `games/rs.json#/lamps/58._note`: Lampz.Callback(83) uses bc83. Bulb above playfield.
- `games/rs.json#/lamps/59._note`: Wig-wag lamp pair. Lampz.Callback(84) = WigWag1. Uses spare lamp IDs 94-95 internally for alternating blink.
- `games/rs.json#/lamps/60._note`: Lampz.Callback(85) uses BobsBunker primitive.
- `games/rs.json#/lamps/61._note`: Wig-wag lamp pair. Lampz.Callback(86) = WigWag2. Uses spare lamp IDs 96-97 internally for alternating blink.
- `games/rs.json#/lamps/62._note`: Lampz.Callback(87) for ExtraballButton and ExtraBallButtonInner.
- `games/rs.json#/lamps/63._note`: Lampz.Callback(88) for StartButton and StartButtonInner.
- `games/rs.json#/_source/confidence_notes`: Re-extracted from VPW 1.4 source (replaces sverrewl-sourced JSON). All switch/coil numbers from _Hit/_UnHit subs, Controller.Switch() calls, PulseSw calls, SolCallback/SolModCallback assignments. No Const sw* definitions in script. Lamp IDs from Lampz.MassAssign() and Lampz.Callback() calls. Trough is custom-implemented (4 switches sw42-sw45 with UpdateTrough timer, no bsTrough object). Slingshots use VPX _Slingshot events with PulseSw 61/62. Jet bumpers use VPX Bumper_Hit events with PulseSw 63/64/65. Flasher coils use SolModCallBack 51-58 (WPC aux board remapped to coils 37-44). Flipper coils use framework constants sLRFlipper=46, sLLFlipper=48. Three left flippers (main + 2 upper via sULFlipper). Bulldozer, Ted jaw, and Red jaw are cvpmMech mechanisms — Road Show's signature talking head mechanisms.

## Unresolved questions

- Is the I/O enumeration complete for every supported physical/controller variant?
- Which inferred VPX behaviors reflect real hardware, and which are table-script conveniences?
- Are all mechanism home states, sensors, motion constraints, and ball interactions documented?

## Sources

- `legacy.game.rs`: `games/rs.json` at the pinned migration revision.
