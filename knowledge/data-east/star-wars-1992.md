# Star Wars

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

- `games/stwr.json#/switches/0._inferred_type`: tilt
- `games/stwr.json#/switches/0._note`: vpmNudge.TiltSwitch = 1
- `games/stwr.json#/switches/1._inferred_type`: trough
- `games/stwr.json#/switches/1._note`: bsTrough.InitSwitches Array(11,13,12,10) — 4th position (jam switch)
- `games/stwr.json#/switches/2._inferred_type`: trough
- `games/stwr.json#/switches/2._note`: bsTrough.InitSwitches Array(11,13,12,10) — 1st position (nearest exit)
- `games/stwr.json#/switches/3._inferred_type`: trough
- `games/stwr.json#/switches/3._note`: bsTrough.InitSwitches Array(11,13,12,10) — 3rd position
- `games/stwr.json#/switches/4._inferred_type`: trough
- `games/stwr.json#/switches/4._note`: bsTrough.InitSwitches Array(11,13,12,10) — 2nd position
- `games/stwr.json#/switches/5._inferred_type`: plunger_lane
- `games/stwr.json#/switches/5._note`: plungerIM.InitImpulseP sw14, 65, 0.5 — auto plunger switch
- `games/stwr.json#/switches/6._inferred_type`: rollover
- `games/stwr.json#/switches/6._note`: vpmTimer.PulseSw 17
- `games/stwr.json#/switches/7._inferred_type`: rollover
- `games/stwr.json#/switches/7._note`: vpmTimer.PulseSw 19
- `games/stwr.json#/switches/8._inferred_type`: ramp_switch
- `games/stwr.json#/switches/8._note`: vpmTimer.PulseSw 20; also calls WireRampOn False
- `games/stwr.json#/switches/9._inferred_type`: rollover
- `games/stwr.json#/switches/9._note`: Controller.Switch(21) on/off — held switch
- `games/stwr.json#/switches/10._inferred_type`: rollover
- `games/stwr.json#/switches/10._note`: Controller.Switch(22) on/off — held switch
- `games/stwr.json#/switches/11._inferred_type`: rollover
- `games/stwr.json#/switches/11._note`: Controller.Switch(23) on/off — held switch
- `games/stwr.json#/switches/12._inferred_type`: rollover
- `games/stwr.json#/switches/12._note`: Controller.Switch(24) on/off — held switch
- `games/stwr.json#/switches/13._inferred_type`: standup_target
- `games/stwr.json#/switches/13._note`: STHit 25 — also in vpmNudge.TiltObj array
- `games/stwr.json#/switches/14._inferred_type`: standup_target
- `games/stwr.json#/switches/14._note`: STHit 26 — also in vpmNudge.TiltObj array
- `games/stwr.json#/switches/15._inferred_type`: standup_target
- `games/stwr.json#/switches/15._note`: STHit 27 — also in vpmNudge.TiltObj array
- `games/stwr.json#/switches/16._inferred_type`: standup_target
- `games/stwr.json#/switches/16._note`: STHit 28
- `games/stwr.json#/switches/17._inferred_type`: standup_target
- `games/stwr.json#/switches/17._note`: STHit 29
- `games/stwr.json#/switches/18._inferred_type`: drop_target
- `games/stwr.json#/switches/18._note`: DTHit 30; reset by sol 6 (ResetDrops)
- `games/stwr.json#/switches/19._inferred_type`: drop_target
- `games/stwr.json#/switches/19._note`: DTHit 31; reset by sol 6 (ResetDrops)
- `games/stwr.json#/switches/20._inferred_type`: drop_target
- `games/stwr.json#/switches/20._note`: DTHit 32; reset by sol 6 (ResetDrops)
- `games/stwr.json#/switches/21._inferred_type`: kicker
- `games/stwr.json#/switches/21._note`: SolRightEject.AddBall 1 — cvpmBallStack InitSaucer sw33, kick angle 220, force 85
- `games/stwr.json#/switches/22._inferred_type`: vuk
- `games/stwr.json#/switches/22._note`: deathstarIn_Hit: DestroyBall, PulseSw 34, AddVUK — ball-destroy/create pattern for Death Star subway
- `games/stwr.json#/switches/23._inferred_type`: vuk
- `games/stwr.json#/switches/23._note`: r2In_Hit: DestroyBall, PulseSw 35, AddVUK — ball-destroy/create pattern for R2D2 subway
- `games/stwr.json#/switches/24._inferred_type`: vuk
- `games/stwr.json#/switches/24._note`: Custom VUK: sw36_Hit destroys ball and AddVUK increments DSBalls counter. Controller.Switch(36) set/cleared by SolLeftPopper (sol 5). Ball-destroy/create pattern.
- `games/stwr.json#/switches/25._inferred_type`: kicker
- `games/stwr.json#/switches/25._note`: SolLeftEject.AddBall 1 — cvpmBallStack InitSaucer sw37, kick angle 163, force 70
- `games/stwr.json#/switches/26._inferred_type`: opto
- `games/stwr.json#/switches/26._note`: Controller.Switch(38) on/off — held switch, likely R2D2 mech position
- `games/stwr.json#/switches/27._inferred_type`: ramp_switch
- `games/stwr.json#/switches/27._note`: vpmTimer.AddTimer 1400 delayed PulseSw 39 — also in vpmNudge.TiltObj array; calls WireRampOff
- `games/stwr.json#/switches/28._inferred_type`: gate
- `games/stwr.json#/switches/28._note`: vpmTimer.PulseSw 40 — also in vpmNudge.TiltObj array; collidable toggled by UpdateDeathStarDoor based on DSDoor.Z position
- `games/stwr.json#/switches/29._inferred_type`: opto
- `games/stwr.json#/switches/29._note`: mechDeathStarDoor.AddSw 41, 0, 0 — mech position switch at step 0 (closed)
- `games/stwr.json#/switches/30._inferred_type`: opto
- `games/stwr.json#/switches/30._note`: mechDeathStarDoor.AddSw 42, 71, 71 — mech position switch at step 71 (fully open)
- `games/stwr.json#/switches/31._inferred_type`: slingshot
- `games/stwr.json#/switches/31._note`: LeftSlingShot_Slingshot: vpmTimer.PulseSw 43
- `games/stwr.json#/switches/32._inferred_type`: slingshot
- `games/stwr.json#/switches/32._note`: RightSlingShot_Slingshot: vpmTimer.PulseSw 44
- `games/stwr.json#/switches/33._inferred_type`: bumper
- `games/stwr.json#/switches/33._note`: vpmTimer.PulseSw(45)
- `games/stwr.json#/switches/34._inferred_type`: bumper
- `games/stwr.json#/switches/34._note`: vpmTimer.PulseSw(46)
- `games/stwr.json#/switches/35._inferred_type`: bumper
- `games/stwr.json#/switches/35._note`: vpmTimer.PulseSw(47)
- `games/stwr.json#/switches/36._inferred_type`: bumper
- `games/stwr.json#/switches/36._note`: vpmTimer.PulseSw(48)
- `games/stwr.json#/switches/37._inferred_type`: cabinet_switch
- `games/stwr.json#/switches/37._note`: Controller.Switch(50) set by PlungerKey/LockBarKey in Table1_KeyDown/KeyUp
- `games/stwr.json#/switches/38._inferred_type`: cabinet_switch
- `games/stwr.json#/switches/38._note`: Controller.Switch(51) set by PlungerKey/LockBarKey and toggled by LeftMagnaSave/RightMagnaSave keys — overloaded for LUT selector in VPW
- `games/stwr.json#/coils/0._vbscript_callback`: bsTroughSolIn
- `games/stwr.json#/coils/0._inferred_type`: trough
- `games/stwr.json#/coils/0._note`: bsTrough.SolIn — feeds ball into trough
- `games/stwr.json#/coils/1._vbscript_callback`: bsTroughSolOut
- `games/stwr.json#/coils/1._inferred_type`: trough
- `games/stwr.json#/coils/1._note`: bsTrough.SolOut — releases ball to shooter lane via BallRelease at angle 90, force 7
- `games/stwr.json#/coils/2._vbscript_callback`: SolAutoPlungerIM
- `games/stwr.json#/coils/2._inferred_type`: autoplunger
- `games/stwr.json#/coils/2._note`: plungerIM.AutoFire — impulse plunger at sw14
- `games/stwr.json#/coils/3._vbscript_callback`: SolLeftEject.SolOut
- `games/stwr.json#/coils/3._inferred_type`: kicker
- `games/stwr.json#/coils/3._note`: cvpmBallStack SolOut — ejects ball from left saucer (sw37)
- `games/stwr.json#/coils/4._vbscript_callback`: SolLeftPopper
- `games/stwr.json#/coils/4._inferred_type`: vuk
- `games/stwr.json#/coils/4._note`: Custom VUK eject: creates ball at sw36, kicks at angle 0/force 45. Manages DSBalls counter and Controller.Switch(36).
- `games/stwr.json#/coils/5._vbscript_callback`: ResetDrops
- `games/stwr.json#/coils/5._inferred_type`: drop_target_reset
- `games/stwr.json#/coils/5._note`: DTRaise 30, 31, 32 — resets all three drop targets
- `games/stwr.json#/coils/6._vbscript_callback`: SolRightEject.SolOut
- `games/stwr.json#/coils/6._inferred_type`: kicker
- `games/stwr.json#/coils/6._note`: cvpmBallStack SolOut — ejects ball from right saucer (sw33)
- `games/stwr.json#/coils/7._vbscript_callback`: SolR2
- `games/stwr.json#/coils/7._inferred_type`: mechanism
- `games/stwr.json#/coils/7._note`: Sets R2UpSol flag controlling R2D2 vertical movement in UpdateR2 timer
- `games/stwr.json#/coils/8._vbscript_callback`: Sol11
- `games/stwr.json#/coils/8._inferred_type`: gi_relay
- `games/stwr.json#/coils/8._note`: SetGI True/False — controls general illumination on/off
- `games/stwr.json#/coils/9._inferred_type`: mechanism
- `games/stwr.json#/coils/9._note`: Commented out SolCallback — handled by mechDeathStarDoor cvpmMech (sol1=12, steps=72, switches 41/42)
- `games/stwr.json#/coils/10._inferred_type`: mechanism
- `games/stwr.json#/coils/10._note`: Commented out SolCallback — handled by mechDeathStar cvpmMech (sol1=15, steps=360, circular motion)
- `games/stwr.json#/coils/11._vbscript_callback`: SolKickback
- `games/stwr.json#/coils/11._inferred_type`: kickback
- `games/stwr.json#/coils/11._note`: Kickback.Fire on enable, Kickback.PullBack on disable
- `games/stwr.json#/coils/12._inferred_type`: bumper
- `games/stwr.json#/coils/12._note`: SolCallback commented out — bumper coil handled natively by VPX Bumper1 object
- `games/stwr.json#/coils/13._inferred_type`: bumper
- `games/stwr.json#/coils/13._note`: SolCallback commented out — bumper coil handled natively by VPX Bumper2 object
- `games/stwr.json#/coils/14._inferred_type`: bumper
- `games/stwr.json#/coils/14._note`: SolCallback commented out — bumper coil handled natively by VPX Bumper3 object
- `games/stwr.json#/coils/15._inferred_type`: bumper
- `games/stwr.json#/coils/15._note`: SolCallback commented out — bumper coil handled natively by VPX Bumper4 object
- `games/stwr.json#/coils/16._inferred_type`: slingshot
- `games/stwr.json#/coils/16._note`: SolCallback commented out — slingshot coil handled natively by VPX LeftSlingShot object
- `games/stwr.json#/coils/17._inferred_type`: slingshot
- `games/stwr.json#/coils/17._note`: SolCallback commented out — slingshot coil handled natively by VPX RightSlingShot object
- `games/stwr.json#/coils/18._vbscript_callback`: Sol25
- `games/stwr.json#/coils/18._inferred_type`: flasher
- `games/stwr.json#/coils/18._note`: SetLamp 125 — routes through Lampz fader. VPX objects: f125a_u, f125a_l, f125b_u, f125b_l, f125c_u, f125c_l, f125d, f125e
- `games/stwr.json#/coils/19._vbscript_callback`: SetLamp 126,
- `games/stwr.json#/coils/19._inferred_type`: flasher
- `games/stwr.json#/coils/19._note`: Direct SetLamp 126. VPX objects: f126a, f126b, f2r
- `games/stwr.json#/coils/20._vbscript_callback`: Sol27
- `games/stwr.json#/coils/20._inferred_type`: flasher
- `games/stwr.json#/coils/20._note`: SetLamp 127. VPX objects: f3r_a, f3r_b
- `games/stwr.json#/coils/21._vbscript_callback`: SetLamp 128,
- `games/stwr.json#/coils/21._inferred_type`: flasher
- `games/stwr.json#/coils/21._note`: Direct SetLamp 128. VPX objects: f128a-d, f4r_a/af/b/bf/c/cf with DisableLighting callbacks pf4_a/b/c
- `games/stwr.json#/coils/22._vbscript_callback`: Sol29
- `games/stwr.json#/coils/22._inferred_type`: flasher
- `games/stwr.json#/coils/22._note`: SetLamp 129. Lampz.MassAssign(129) commented out — Death Star flasher
- `games/stwr.json#/coils/23._vbscript_callback`: Sol30
- `games/stwr.json#/coils/23._inferred_type`: flasher
- `games/stwr.json#/coils/23._note`: SetLamp 130. VPX objects: f6r_a, f6r_b
- `games/stwr.json#/coils/24._vbscript_callback`: Sol31
- `games/stwr.json#/coils/24._inferred_type`: flasher
- `games/stwr.json#/coils/24._note`: SetLamp 131. Lampz.MassAssign(131) commented out — R2D2 flasher
- `games/stwr.json#/coils/25._vbscript_callback`: SetLamp 132,
- `games/stwr.json#/coils/25._inferred_type`: flasher
- `games/stwr.json#/coils/25._note`: Direct SetLamp 132. VPX objects: F132a-e, f8r_a/b/f with DisableLighting callbacks pf8_a/b
- `games/stwr.json#/coils/26._vbscript_callback`: SolRFlipper
- `games/stwr.json#/coils/26._inferred_type`: flipper
- `games/stwr.json#/coils/26._note`: sLRFlipper framework constant from DE.VBS/core.vbs
- `games/stwr.json#/coils/27._vbscript_callback`: SolLFlipper
- `games/stwr.json#/coils/27._inferred_type`: flipper
- `games/stwr.json#/coils/27._note`: sLLFlipper framework constant from DE.VBS/core.vbs
- `games/stwr.json#/lamps/43._note`: Lampz.MassAssign(48) commented out; callback to JabbasInsert DisableLighting
- `games/stwr.json#/lamps/60._note`: Lampz.obj(111) = ColtoArray(GI) — GI collection, controlled by sol 11 relay
- `games/stwr.json#/_source/confidence_notes`: High confidence on switches/coils from VPW v1.2.2 script. Trough is standard cvpmTrough with 4-switch array (11,13,12,10). Death Star uses two cvpmMech objects: mechDeathStarDoor (sol 12, switches 41/42) and mechDeathStar rotation (sol 15). Death Star VUK (sw36) uses custom ball-destroy/create pattern with DSBalls counter. R2D2 entrance (sw35) also uses ball-destroy pattern. Flashers (sol 25-32) route through Lampz fader as IDs 125-132. Bumper coils 17-20 and slingshot coils 21-22 are commented out in SolCallback (handled natively by VPX physics objects). Switch 50 = launch button, switch 51 = magna save (overloaded for LUT selector in VPW). GI controlled via sol 11 relay. DE.VBS framework: sLRFlipper=46, sLLFlipper=48.

## Unresolved questions

- Is the I/O enumeration complete for every supported physical/controller variant?
- Which inferred VPX behaviors reflect real hardware, and which are table-script conveniences?
- Are all mechanism home states, sensors, motion constraints, and ball interactions documented?

## Sources

- `legacy.game.stwr`: `games/stwr.json` at the pinned migration revision.
