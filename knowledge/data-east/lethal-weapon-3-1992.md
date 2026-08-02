# Lethal Weapon 3

Coverage: **partial - source-derived recreation knowledge requiring validation**

## Overview

Legacy evidence identifies this candidate as Data East (1992). The information below is preserved for recreation work but is not automatically treated as validated physical-machine fact.

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

- `games/lw3.json#/switches/0._note`: vpmNudge.TiltSwitch = 1
- `games/lw3.json#/switches/1._note`: Controller.Switch(9) set by PlungerKey and LockBarKey
- `games/lw3.json#/switches/2._note`: Drain entry — Controller.Switch(10), UpdateTrough cascade. SolTrough kicks this toward shooter lane.
- `games/lw3.json#/switches/3._note`: Trough position 1 (closest to drain) — Controller.Switch(11)
- `games/lw3.json#/switches/4._note`: Trough position 2 — Controller.Switch(12)
- `games/lw3.json#/switches/5._note`: Trough position 3 (deepest) — SolRelease kicks from here. Balls created here at init.
- `games/lw3.json#/switches/6._note`: plungerIM.switch = 14 (cvpmImpulseP); Autofire sol 12 calls plungerIM.AutoFire
- `games/lw3.json#/switches/7._note`: Controller.Switch(15) set by LeftFlipperKey
- `games/lw3.json#/switches/8._note`: Controller.Switch(16) set by RightFlipperKey
- `games/lw3.json#/switches/9._inferred_type`: standup_target
- `games/lw3.json#/switches/9._note`: STHit 17
- `games/lw3.json#/switches/10._inferred_type`: standup_target
- `games/lw3.json#/switches/10._note`: STHit 18
- `games/lw3.json#/switches/11._inferred_type`: standup_target
- `games/lw3.json#/switches/11._note`: STHit 19
- `games/lw3.json#/switches/12._inferred_type`: standup_target
- `games/lw3.json#/switches/12._note`: STHit 20
- `games/lw3.json#/switches/13._inferred_type`: rollover
- `games/lw3.json#/switches/13._note`: Controller.Switch(21) via Sw21_Hit/Sw21_UnHit
- `games/lw3.json#/switches/14._inferred_type`: rollover
- `games/lw3.json#/switches/14._note`: Controller.Switch(22) via Sw22_Hit/Sw22_UnHit
- `games/lw3.json#/switches/15._inferred_type`: drop_target
- `games/lw3.json#/switches/15._note`: DTDrop via DTArray, reset by dtMSolDropUp (sol 6)
- `games/lw3.json#/switches/16._inferred_type`: drop_target
- `games/lw3.json#/switches/16._note`: DTDrop via DTArray, reset by dtMSolDropUp (sol 6)
- `games/lw3.json#/switches/17._inferred_type`: drop_target
- `games/lw3.json#/switches/17._note`: DTDrop via DTArray, reset by dtMSolDropUp (sol 6)
- `games/lw3.json#/switches/18._inferred_type`: rollover
- `games/lw3.json#/switches/18._note`: Controller.Switch(28) via Sw28_Hit/Sw28_UnHit
- `games/lw3.json#/switches/19._inferred_type`: rollover
- `games/lw3.json#/switches/19._note`: Controller.Switch(29), triggers leftInlaneSpeedLimit
- `games/lw3.json#/switches/20._inferred_type`: slingshot
- `games/lw3.json#/switches/20._note`: vpmTimer.PulseSw 30 in LeftSlingShot_Slingshot
- `games/lw3.json#/switches/21._inferred_type`: vuk
- `games/lw3.json#/switches/21._note`: sw31_Hit sets Controller.switch(31)=1; VukTopPop (sol 15) kicks via sw31.KickZ
- `games/lw3.json#/switches/22._inferred_type`: kicker
- `games/lw3.json#/switches/22._note`: bsLock2.InitSaucer sw32; sw32_Hit calls bsLock2.AddBall
- `games/lw3.json#/switches/23._inferred_type`: drop_target
- `games/lw3.json#/switches/23._note`: DTDrop via DTArray, reset by dtRSolDropUp (sol 7)
- `games/lw3.json#/switches/24._inferred_type`: drop_target
- `games/lw3.json#/switches/24._note`: DTDrop via DTArray, reset by dtRSolDropUp (sol 7)
- `games/lw3.json#/switches/25._inferred_type`: drop_target
- `games/lw3.json#/switches/25._note`: DTDrop via DTArray, reset by dtRSolDropUp (sol 7)
- `games/lw3.json#/switches/26._inferred_type`: rollover
- `games/lw3.json#/switches/26._note`: Controller.Switch(36) via Sw36_Hit/Sw36_UnHit
- `games/lw3.json#/switches/27._inferred_type`: rollover
- `games/lw3.json#/switches/27._note`: Controller.Switch(37), triggers rightInlaneSpeedLimit
- `games/lw3.json#/switches/28._inferred_type`: slingshot
- `games/lw3.json#/switches/28._note`: vpmTimer.PulseSw 38 in RightSlingShot_Slingshot
- `games/lw3.json#/switches/29._inferred_type`: standup_target
- `games/lw3.json#/switches/29._note`: STHit 39
- `games/lw3.json#/switches/30._inferred_type`: kicker
- `games/lw3.json#/switches/30._note`: bsLock.InitSaucer sw40; sw40_Hit calls bsLock.AddBall
- `games/lw3.json#/switches/31._inferred_type`: rollover
- `games/lw3.json#/switches/31._note`: Controller.Switch(41) via Sw41_Hit/Sw41_UnHit
- `games/lw3.json#/switches/32._inferred_type`: rollover
- `games/lw3.json#/switches/32._note`: Controller.Switch(42) via Sw42_Hit/Sw42_UnHit
- `games/lw3.json#/switches/33._inferred_type`: rollover
- `games/lw3.json#/switches/33._note`: Controller.Switch(43) via Sw43_Hit/Sw43_UnHit
- `games/lw3.json#/switches/34._inferred_type`: bumper
- `games/lw3.json#/switches/34._note`: vpmTimer.PulseSw 44 in Bumper1_Hit
- `games/lw3.json#/switches/35._inferred_type`: bumper
- `games/lw3.json#/switches/35._note`: vpmTimer.PulseSw 45 in Bumper2_Hit
- `games/lw3.json#/switches/36._inferred_type`: bumper
- `games/lw3.json#/switches/36._note`: vpmTimer.PulseSw 46 in Bumper3_Hit
- `games/lw3.json#/switches/37._inferred_type`: spinner
- `games/lw3.json#/switches/37._note`: vpmTimer.PulseSw 47 in Sw47_Spin
- `games/lw3.json#/switches/38._inferred_type`: spinner
- `games/lw3.json#/switches/38._note`: vpmTimer.PulseSw 48 in Sw48_Spin
- `games/lw3.json#/switches/39._inferred_type`: rollover
- `games/lw3.json#/switches/39._note`: vpmTimer.PulseSw 49 in Sw49_Hit
- `games/lw3.json#/switches/40._inferred_type`: rollover
- `games/lw3.json#/switches/40._note`: vpmTimer.PulseSw 50 in Sw50_Hit
- `games/lw3.json#/switches/41._inferred_type`: rollover
- `games/lw3.json#/switches/41._note`: Controller.Switch(52) via Sw52_Hit/Sw52_UnHit
- `games/lw3.json#/switches/42._inferred_type`: rollover
- `games/lw3.json#/switches/42._note`: Controller.Switch(54) via Sw54_Hit/Sw54_UnHit
- `games/lw3.json#/switches/43._inferred_type`: rollover
- `games/lw3.json#/switches/43._note`: Controller.Switch(55) via Sw55_Hit/Sw55_UnHit
- `games/lw3.json#/coils/0._vbscript_callback`: SolTrough
- `games/lw3.json#/coils/0._inferred_type`: ball_management
- `games/lw3.json#/coils/0._note`: Kicks sw10 with force 60/angle 30 — pushes ball from drain entry toward trough stack
- `games/lw3.json#/coils/1._vbscript_callback`: SolRelease
- `games/lw3.json#/coils/1._inferred_type`: ball_management
- `games/lw3.json#/coils/1._note`: Kicks sw13 with force 60/angle 10 — releases ball from deepest trough position to shooter lane
- `games/lw3.json#/coils/2._vbscript_callback`: bsLock.SolOut
- `games/lw3.json#/coils/2._inferred_type`: ball_management
- `games/lw3.json#/coils/2._note`: cvpmBallStack release — bsLock.InitSaucer sw40, angle 165, force 17
- `games/lw3.json#/coils/3._vbscript_callback`: bsLock2.SolOut
- `games/lw3.json#/coils/3._inferred_type`: ball_management
- `games/lw3.json#/coils/3._note`: cvpmBallStack release — bsLock2.InitSaucer sw32, angle 280, force 17
- `games/lw3.json#/coils/4._vbscript_callback`: dtMSolDropUp
- `games/lw3.json#/coils/4._inferred_type`: drop_target_reset
- `games/lw3.json#/coils/4._note`: Resets drop targets sw25, sw26, sw27 via DTRaise
- `games/lw3.json#/coils/5._vbscript_callback`: dtRSolDropUp
- `games/lw3.json#/coils/5._inferred_type`: drop_target_reset
- `games/lw3.json#/coils/5._note`: Resets drop targets sw33, sw34, sw35 via DTRaise
- `games/lw3.json#/coils/6._vbscript_callback`: SolKnocker
- `games/lw3.json#/coils/6._inferred_type`: knocker
- `games/lw3.json#/coils/7._vbscript_callback`: Sol09
- `games/lw3.json#/coils/7._inferred_type`: flasher
- `games/lw3.json#/coils/7._note`: SolModCallback; controls F109.state and F109a.state
- `games/lw3.json#/coils/8._vbscript_callback`: SolRelayGI
- `games/lw3.json#/coils/8._inferred_type`: mechanism
- `games/lw3.json#/coils/8._note`: SolModCallback; controls GI collection state and pSpotBulbs opacity. DE A-relay for general illumination.
- `games/lw3.json#/coils/9._vbscript_callback`: Autofire
- `games/lw3.json#/coils/9._inferred_type`: ball_management
- `games/lw3.json#/coils/9._note`: Calls plungerIM.AutoFire (cvpmImpulseP) — fires ball from shooter lane
- `games/lw3.json#/coils/10._vbscript_callback`: SolRotateBeacons
- `games/lw3.json#/coils/10._inferred_type`: mechanism
- `games/lw3.json#/coils/10._note`: Enables BeaconTimer and toggles BeaconBlue image
- `games/lw3.json#/coils/11._vbscript_callback`: VukTopPop
- `games/lw3.json#/coils/11._inferred_type`: ball_management
- `games/lw3.json#/coils/11._note`: Kicks sw31 via KickZ — vertical upkicker
- `games/lw3.json#/coils/12._vbscript_callback`: Sol16
- `games/lw3.json#/coils/12._inferred_type`: flasher
- `games/lw3.json#/coils/12._note`: SolModCallback; controls F116.state
- `games/lw3.json#/coils/13._vbscript_callback`: SolKickback
- `games/lw3.json#/coils/13._inferred_type`: mechanism
- `games/lw3.json#/coils/13._note`: kickback.fire when enabled, kickback.pullback when disabled
- `games/lw3.json#/coils/14._vbscript_callback`: Flash1R
- `games/lw3.json#/coils/14._inferred_type`: flasher
- `games/lw3.json#/coils/14._note`: SolModCallback; 1R PF — BG Mel Top
- `games/lw3.json#/coils/15._vbscript_callback`: Flash2R
- `games/lw3.json#/coils/15._inferred_type`: flasher
- `games/lw3.json#/coils/15._note`: SolModCallback; controls F126.state, F126a.state
- `games/lw3.json#/coils/16._vbscript_callback`: Flash3R
- `games/lw3.json#/coils/16._inferred_type`: flasher
- `games/lw3.json#/coils/16._note`: SolModCallback; BG Bottom Left Rails — controls F127.state, F127a.state
- `games/lw3.json#/coils/17._vbscript_callback`: Flash4R
- `games/lw3.json#/coils/17._inferred_type`: flasher
- `games/lw3.json#/coils/17._note`: SolModCallback; controls F128.state, F128a.state, F128b.state
- `games/lw3.json#/coils/18._vbscript_callback`: Flash5R
- `games/lw3.json#/coils/18._inferred_type`: flasher
- `games/lw3.json#/coils/18._note`: SolModCallback; BG Mel Bottom — controls F129.state, F129a.state
- `games/lw3.json#/coils/19._vbscript_callback`: Flash6R
- `games/lw3.json#/coils/19._inferred_type`: flasher
- `games/lw3.json#/coils/19._note`: SolModCallback; controls F130.state, F130a-c.state
- `games/lw3.json#/coils/20._vbscript_callback`: Flash7R
- `games/lw3.json#/coils/20._inferred_type`: flasher
- `games/lw3.json#/coils/20._note`: SolModCallback; BG Left 1 — controls F131.state
- `games/lw3.json#/coils/21._vbscript_callback`: Flash8R
- `games/lw3.json#/coils/21._inferred_type`: flasher
- `games/lw3.json#/coils/21._note`: SolModCallback; BG Left 2 — controls F132.state, F132a.state. Note: sol 32 appears assigned twice in script (duplicate line).
- `games/lw3.json#/coils/22._vbscript_callback`: SolRFlipper
- `games/lw3.json#/coils/22._inferred_type`: flipper
- `games/lw3.json#/coils/22._note`: sLRFlipper from DE.VBS framework (core.vbs constant = 46)
- `games/lw3.json#/coils/23._vbscript_callback`: SolLFlipper
- `games/lw3.json#/coils/23._inferred_type`: flipper
- `games/lw3.json#/coils/23._note`: sLLFlipper from DE.VBS framework (core.vbs constant = 48)
- `games/lw3.json#/lamps/42._note`: LM_FL_L44 — flasher-style lamp (driven via lamp matrix, not solenoid)
- `games/lw3.json#/_source/confidence_notes`: High confidence on switches/coils from VPW 2.0 script. Trough is manual (no bsTrough/cvpmTrough) — uses direct Controller.Switch calls on sw10-sw13 with custom UpdateTrough cascading logic. 3 balls, sw13=deepest, sw10=drain entry. SolTrough(1) kicks sw10 toward shooter, SolRelease(2) kicks sw13 (ball release). Two ball locks via cvpmBallStack: bsLock(sw40, sol 4) and bsLock2(sw32, sol 5). Auto-plunger via cvpmImpulseP on swplunger with .switch=14. Lamp IDs from VLM array naming convention (LM_IN_L##); lamp descriptions unavailable without manual — IDs only. Flasher VPX names from Flash*R handler bodies (F125-F132, F109, F116). DE platform from LoadVPM 'DE.VBS'. Flipper solenoid IDs (sLRFlipper=46, sLLFlipper=48) are DE.VBS framework constants. Sol 32 appears assigned twice (Flash8R) in script — likely a copy error, second line is duplicate.

## Unresolved questions

- Is the I/O enumeration complete for every supported physical/controller variant?
- Which inferred VPX behaviors reflect real hardware, and which are table-script conveniences?
- Are all mechanism home states, sensors, motion constraints, and ball interactions documented?

## Sources

- `legacy.game.lw3`: `games/lw3.json` at the pinned migration revision.
