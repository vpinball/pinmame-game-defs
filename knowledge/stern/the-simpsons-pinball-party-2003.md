# The Simpsons Pinball Party

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

- `games/simp.json#/switches/0._note`: Controller.Switch(6) on/off from AddCreditKey KeyDown/KeyUp
- `games/simp.json#/switches/1._note`: PulseSw 9
- `games/simp.json#/switches/2._note`: bsTrough.InitSw — position 5 (last switch in 5-ball trough)
- `games/simp.json#/switches/3._note`: bsTrough.InitSw — position 4
- `games/simp.json#/switches/4._note`: bsTrough.InitSw — position 3
- `games/simp.json#/switches/5._note`: bsTrough.InitSw — position 2
- `games/simp.json#/switches/6._note`: bsTrough.InitSw — position 1 (first to eject)
- `games/simp.json#/switches/7._note`: PulseSw 15 fired in SolRelease after trough eject
- `games/simp.json#/switches/8._note`: Controller.Switch on/off. Also used by plungerIM (cvpmImpulseP) as plunger lane switch. BIPL flag tracks ball-in-plunger-lane.
- `games/simp.json#/switches/9._note`: dtDrop.InitDrop Array(sw17,sw18,sw19), Array(17,18,19). VPX drop target object.
- `games/simp.json#/switches/10._note`: dtDrop.InitDrop
- `games/simp.json#/switches/11._note`: dtDrop.InitDrop
- `games/simp.json#/switches/12._note`: bsBR cvpmBallStack. InitSaucer sw20, 20, 232, 30. Ball management.
- `games/simp.json#/switches/13._note`: PulseSw 21 on sw21_Spin event
- `games/simp.json#/switches/14._note`: Controller.Switch on/off — opto-style (held while ball present)
- `games/simp.json#/switches/15._note`: Controller.Switch on/off — opto-style (held while ball present)
- `games/simp.json#/switches/16._note`: bsTR cvpmBallStack. InitSaucer sw24, 24, 100, 1. Ball management.
- `games/simp.json#/switches/17._note`: Controller.Switch on/off
- `games/simp.json#/switches/18._note`: Controller.Switch on/off
- `games/simp.json#/switches/19._note`: Controller.Switch on/off
- `games/simp.json#/switches/20._note`: PulseSw 30
- `games/simp.json#/switches/21._note`: PulseSw 31
- `games/simp.json#/switches/22._note`: PulseSw 32
- `games/simp.json#/switches/23._note`: PulseSw 33
- `games/simp.json#/switches/24._note`: PulseSw 34
- `games/simp.json#/switches/25._note`: PulseSw 35
- `games/simp.json#/switches/26._note`: PulseSw 36. Also triggers WireRampOn/Off sound based on ball direction.
- `games/simp.json#/switches/27._note`: Controller.Switch on/off
- `games/simp.json#/switches/28._note`: Controller.Switch on/off. Also referenced by CouchDrop_Hit (sets switch 38=0). Drop1 object.
- `games/simp.json#/switches/29._note`: Controller.Switch on/off. Drop2 object.
- `games/simp.json#/switches/30._note`: Controller.Switch on/off. Ball lands on couch after drop. Turns off WireRamp sound.
- `games/simp.json#/switches/31._note`: PulseSw 41
- `games/simp.json#/switches/32._note`: PulseSw 42
- `games/simp.json#/switches/33._note`: PulseSw 43
- `games/simp.json#/switches/34._note`: Controller.Switch on/off
- `games/simp.json#/switches/35._note`: PulseSw 45
- `games/simp.json#/switches/36._note`: PulseSw 46
- `games/simp.json#/switches/37._note`: PulseSw 47
- `games/simp.json#/switches/38._note`: PulseSw 48. Comment says 'Garage Door'.
- `games/simp.json#/switches/39._note`: PulseSw 49 in Bumper3_Hit
- `games/simp.json#/switches/40._note`: PulseSw 50 in Bumper1_Hit
- `games/simp.json#/switches/41._note`: PulseSw 51 in Bumper2_Hit
- `games/simp.json#/switches/42._note`: PulseSw 52
- `games/simp.json#/switches/43._note`: Controller.Switch(54) on/off from StartGameKey KeyDown/KeyUp
- `games/simp.json#/switches/44._note`: bsVuk cvpmBallStack. InitSw 0,55. Ball management — ball enters via sw55_Hit, exits via VukOut kicker.
- `games/simp.json#/switches/45._note`: Controller.Switch on/off
- `games/simp.json#/switches/46._note`: Controller.Switch on/off
- `games/simp.json#/switches/47._note`: PulseSw 59 in LeftSlingShot_Slingshot sub
- `games/simp.json#/switches/48._note`: Controller.Switch on/off
- `games/simp.json#/switches/49._note`: Controller.Switch on/off
- `games/simp.json#/switches/50._note`: PulseSw 62 in RightSlingShot_Slingshot sub
- `games/simp.json#/switches/51._note`: Controller.Switch on/off
- `games/simp.json#/switches/52._note`: Controller.Switch on/off
- `games/simp.json#/coils/0._vbscript_callback`: SolRelease
- `games/simp.json#/coils/0._inferred_type`: ball_management
- `games/simp.json#/coils/0._note`: Fires bsTrough.ExitSol_On then PulseSw 15 (shooter lane confirm). Kick angle 45, force 9.
- `games/simp.json#/coils/1._vbscript_callback`: Auto_Plunger
- `games/simp.json#/coils/1._inferred_type`: ball_management
- `games/simp.json#/coils/1._note`: cvpmImpulseP. plungerIM.AutoFire. Power=75, Time=0.7s.
- `games/simp.json#/coils/2._vbscript_callback`: CouchExit
- `games/simp.json#/coils/2._inferred_type`: ball_management
- `games/simp.json#/coils/2._note`: Enables CouchDrop timer to release ball from couch lock. Drop1 reset logic. Original comment: vlLock.SolExit.
- `games/simp.json#/coils/3._vbscript_callback`: dtDrop.SolDropUp
- `games/simp.json#/coils/3._inferred_type`: drop_target
- `games/simp.json#/coils/3._note`: Resets drop targets sw17/sw18/sw19. Also clears blenddisablelighting on SW17/SW18/SW19 objects. Inline callback expression.
- `games/simp.json#/coils/4._vbscript_callback`: bsBR.SolOut
- `games/simp.json#/coils/4._inferred_type`: ball_management
- `games/simp.json#/coils/4._note`: bsBR cvpmBallStack eject. Kick angle 232, force 30.
- `games/simp.json#/coils/5._vbscript_callback`: bsVUK.SolOut
- `games/simp.json#/coils/5._inferred_type`: ball_management
- `games/simp.json#/coils/5._note`: bsVuk cvpmBallStack eject via VukOut kicker. Kick angle 180, force 0 (vertical).
- `games/simp.json#/coils/6._vbscript_callback`: SolTVRelease
- `games/simp.json#/coils/6._inferred_type`: mechanism
- `games/simp.json#/coils/6._note`: Drops/raises TopPost. When enabled: TopPost.IsDropped=1 (releases ball). When disabled: TopPost.IsDropped=0 (blocks).
- `games/simp.json#/coils/7._vbscript_callback`: SolHomer
- `games/simp.json#/coils/7._inferred_type`: mechanism
- `games/simp.json#/coils/7._note`: Rotates Homer head mechanism. Enabled: HomerActive=1, rotates head up (HeadDir=2). Disabled: rotates head down (HeadDir=-2). Uses HeadTimer for animation.
- `games/simp.json#/coils/8._vbscript_callback`: SolTopLeftFlipper
- `games/simp.json#/coils/8._inferred_type`: flipper
- `games/simp.json#/coils/8._note`: ROM-controlled upper left flipper. Only fires when LFPress=0 (no player button press).
- `games/simp.json#/coils/9._vbscript_callback`: SolTopRightFlipper
- `games/simp.json#/coils/9._inferred_type`: flipper
- `games/simp.json#/coils/9._note`: ROM-controlled upper right flipper. Only fires when RFPress=0.
- `games/simp.json#/coils/10._vbscript_callback`: SolRightFlipper2
- `games/simp.json#/coils/10._inferred_type`: flipper
- `games/simp.json#/coils/10._note`: ROM-controlled secondary right flipper. Only fires when RFPress=0.
- `games/simp.json#/coils/11._vbscript_callback`: bsTR.SolOut
- `games/simp.json#/coils/11._inferred_type`: ball_management
- `games/simp.json#/coils/11._note`: bsTR cvpmBallStack eject. Kick angle 100, force 1.
- `games/simp.json#/coils/12._vbscript_callback`: GarageUp
- `games/simp.json#/coils/12._inferred_type`: mechanism
- `games/simp.json#/coils/12._note`: Opens/closes garage door mechanism. Enabled: DoorStatus=1 (opens). Disabled: DoorStatus=0 (closes). Uses GDoorT timer for animation.
- `games/simp.json#/coils/13._vbscript_callback`: FlashPops
- `games/simp.json#/coils/13._inferred_type`: flasher
- `games/simp.json#/coils/13._note`: FlupperDoms v2 flasher. ObjTargetLevel(1).
- `games/simp.json#/coils/14._vbscript_callback`: RightRampRed
- `games/simp.json#/coils/14._inferred_type`: flasher
- `games/simp.json#/coils/14._note`: FlupperDoms v2 flasher. ObjTargetLevel(4).
- `games/simp.json#/coils/15._vbscript_callback`: DuffCan
- `games/simp.json#/coils/15._inferred_type`: flasher
- `games/simp.json#/coils/15._note`: FlupperDoms v2 flasher. ObjTargetLevel(5). Comment: R.Ramp Orange / Duff Can.
- `games/simp.json#/coils/16._vbscript_callback`: FlashItchy
- `games/simp.json#/coils/16._inferred_type`: flasher
- `games/simp.json#/coils/16._note`: FlupperDoms v2 flasher. ObjTargetLevel(6).
- `games/simp.json#/coils/17._vbscript_callback`: FlashScratchy
- `games/simp.json#/coils/17._inferred_type`: flasher
- `games/simp.json#/coils/17._note`: FlupperDoms v2 flasher. ObjTargetLevel(8).
- `games/simp.json#/coils/18._vbscript_callback`: HomerHead
- `games/simp.json#/coils/18._inferred_type`: flasher
- `games/simp.json#/coils/18._note`: FlupperDoms v2 flasher. ObjTargetLevel(10). Illuminates Homer head mechanism.
- `games/simp.json#/coils/19._vbscript_callback`: FlashCouch
- `games/simp.json#/coils/19._inferred_type`: flasher
- `games/simp.json#/coils/19._note`: FlupperDoms v2 flasher. ObjTargetLevel(2).
- `games/simp.json#/coils/20._vbscript_callback`: FlashCBG
- `games/simp.json#/coils/20._inferred_type`: flasher
- `games/simp.json#/coils/20._note`: FlupperDoms v2 flasher. ObjTargetLevel(9).
- `games/simp.json#/coils/21._vbscript_callback`: SolDropBankTrips
- `games/simp.json#/coils/21._inferred_type`: drop_target
- `games/simp.json#/coils/21._note`: Knocks down all 3 drops in bank (dtDrop.Hit 1/2/3). Sets blenddisablelighting on SW17/SW18/SW19.
- `games/simp.json#/coils/22._vbscript_callback`: UPFOrange
- `games/simp.json#/coils/22._inferred_type`: flasher
- `games/simp.json#/coils/22._note`: FlupperDoms v2 flasher. ObjTargetLevel(7).
- `games/simp.json#/coils/23._vbscript_callback`: UPFRed
- `games/simp.json#/coils/23._inferred_type`: flasher
- `games/simp.json#/coils/23._note`: FlupperDoms v2 flasher. ObjTargetLevel(3).
- `games/simp.json#/lamps/0._note`: Also bl1 (bloom layer). Callback: DisableLighting p1.
- `games/simp.json#/lamps/1._note`: Also bl2. Callback: DisableLighting p2.
- `games/simp.json#/lamps/2._note`: Also bl3. Callback: DisableLighting p3.
- `games/simp.json#/lamps/3._note`: Also bl4. Callback: DisableLighting p4.
- `games/simp.json#/lamps/4._note`: Also bl5. Callback: DisableLighting p5.
- `games/simp.json#/lamps/5._note`: Also bl6. Callback: DisableLighting p6.
- `games/simp.json#/lamps/6._note`: Also bl7. Callback: DisableLighting p7.
- `games/simp.json#/lamps/7._note`: Also bl8. Callback: DisableLighting p8.
- `games/simp.json#/lamps/8._note`: Also bl9. Callback: DisableLighting p9.
- `games/simp.json#/lamps/9._note`: Also bl10. Callback: DisableLighting p10.
- `games/simp.json#/lamps/10._note`: Also bl11. Callback: DisableLighting p11.
- `games/simp.json#/lamps/11._note`: Also bl12. Callback: DisableLighting p12.
- `games/simp.json#/lamps/12._note`: Also bl13. Callback: DisableLighting p13.
- `games/simp.json#/lamps/13._note`: Also bl14. Callback: DisableLighting p14.
- `games/simp.json#/lamps/14._note`: Also bl15. Callback: DisableLighting p15.
- `games/simp.json#/lamps/17._note`: Bumper 1 lamp. Callback: bump1LitOpacity.
- `games/simp.json#/lamps/18._note`: Bumper 2 lamp. Callback: bump2LitOpacity.
- `games/simp.json#/lamps/19._note`: Also bl20. Callback: DisableLighting p20.
- `games/simp.json#/lamps/20._note`: Also bl21. Callback: DisableLighting p21.
- `games/simp.json#/lamps/21._note`: Also bl22. Callback: DisableLighting p22.
- `games/simp.json#/lamps/22._note`: Also bl23. Callback: DisableLighting p23.
- `games/simp.json#/lamps/23._note`: Also bl24. Callback: DisableLighting p24.
- `games/simp.json#/lamps/24._note`: Also bl25. Callback: DisableLighting p25.
- `games/simp.json#/lamps/25._note`: Also bl26. Callback: DisableLighting p26.
- `games/simp.json#/lamps/26._note`: Also bl27. Callback: DisableLighting p27.
- `games/simp.json#/lamps/27._note`: Also bl28. Callback: DisableLighting p28.
- `games/simp.json#/lamps/28._note`: Also bl29. Callback: DisableLighting p29.
- `games/simp.json#/lamps/29._note`: Also bl30. Callback: DisableLighting p30.
- `games/simp.json#/lamps/31._note`: Also bl33. Callback: DisableLighting p33.
- `games/simp.json#/lamps/32._note`: Also bl34. Callback: DisableLighting p34.
- `games/simp.json#/lamps/33._note`: Also bl35. Callback: DisableLighting p35.
- `games/simp.json#/lamps/34._note`: Also bl36. Callback: DisableLighting p36.
- `games/simp.json#/lamps/35._note`: Also bl37. Callback: DisableLighting p37.
- `games/simp.json#/lamps/36._note`: Also bl38. Callback: DisableLighting p38.
- `games/simp.json#/lamps/37._note`: Also bl39. Callback: DisableLighting p39.
- `games/simp.json#/lamps/38._note`: Also bl40. Callback: DisableLighting p40.
- `games/simp.json#/lamps/39._note`: Also bl41. Callback: DisableLighting p41.
- `games/simp.json#/lamps/40._note`: Also bl42. Callback: DisableLighting p42.
- `games/simp.json#/lamps/41._note`: Also bl43. Callback: DisableLighting p43.
- `games/simp.json#/lamps/42._note`: Also bl44. Callback: DisableLighting p44.
- `games/simp.json#/lamps/43._note`: Also bl45. Callback: DisableLighting p45.
- `games/simp.json#/lamps/44._note`: Also bl46. Callback: DisableLighting p46.
- `games/simp.json#/lamps/45._note`: Also bl47. Callback: DisableLighting p47.
- `games/simp.json#/lamps/46._note`: Also bl48. Callback: DisableLighting p48.
- `games/simp.json#/lamps/47._note`: Also bl49. Callback: DisableLighting p49.
- `games/simp.json#/lamps/48._note`: Also bl50. Callback: DisableLighting p50.
- `games/simp.json#/lamps/49._note`: Also bl51. Callback: DisableLighting p51.
- `games/simp.json#/lamps/50._note`: Also bl52. Callback: DisableLighting p52.
- `games/simp.json#/lamps/51._note`: Also bl53. Callback: DisableLighting p53.
- `games/simp.json#/lamps/52._note`: Also bl54. Callback: DisableLighting p54.
- `games/simp.json#/lamps/53._note`: Also bl55. Callback: DisableLighting p55.
- `games/simp.json#/lamps/54._note`: Also bl56. Callback: DisableLighting p56.
- `games/simp.json#/lamps/61._note`: Also bl63. Callback: DisableLighting p63.
- `games/simp.json#/lamps/62._note`: Also bl64. Callback: DisableLighting p64.
- `games/simp.json#/lamps/63._note`: Also bl65. Callback: DisableLighting p65.
- `games/simp.json#/lamps/64._note`: Also bl66. Callback: DisableLighting p66.
- `games/simp.json#/lamps/65._note`: Also bl67. Callback: DisableLighting p67.
- `games/simp.json#/lamps/66._note`: Also bl68. Callback: DisableLighting p68.
- `games/simp.json#/lamps/67._note`: Also bl69. Callback: DisableLighting p69.
- `games/simp.json#/lamps/68._note`: Also bl70. Callback: DisableLighting p70.
- `games/simp.json#/lamps/69._note`: Callback only (no MassAssign). DisableLighting l73, 150.
- `games/simp.json#/lamps/70._note`: Callback only. DisableLighting l74, 145.
- `games/simp.json#/lamps/71._note`: Callback only. DisableLighting l75, 140.
- `games/simp.json#/lamps/72._note`: Callback only. DisableLighting l76, 135.
- `games/simp.json#/lamps/73._note`: Callback only. DisableLighting l77, 130.
- `games/simp.json#/lamps/74._note`: Callback only. DisableLighting l78, 125.
- `games/simp.json#/lamps/75._note`: Callback only. DisableLighting l79, 125.
- `games/simp.json#/lamps/76._note`: Callback only. DisableLighting l80/l80b, 5. Two callback lines — likely two VPX objects.
- `games/simp.json#/lamps/77._note`: Lampz.obj(111) = ColtoArray(GI). Mapped to GI collection. Callback: GIUpdates. Controls backglass brightness in VR mode.
- `games/simp.json#/_source/confidence_notes`: High confidence on switches/coils. No Const sw* definitions in script — switches identified from _Hit/_UnHit subs, Controller.Switch() calls, PulseSw calls, and cvpmBallStack/cvpmDropTarget init. swTilt comes from Sega.VBS framework (not defined in table script) — documented but not assigned a number here. Flasher coils (21-29, 31-32) use SolCallBack with custom Flash subs and FlupperDoms v2 flasher system. Lamps use Lampz (LampFader class) with MassAssign. UseSolenoids=2 (FastFlips), UseLamps=0, UseGI=0. Complex game: 5-ball trough, 3 ball stacks (bsBR, bsTR, bsVUK), drop target bank (3 targets), Homer head mechanism (solenoid 8), garage door mechanism (solenoid 20), TV lock post (solenoid 7), couch lock/exit (solenoid 3). Lamp 111 is GI (mapped to GI collection). Lamps 73-80 have callbacks but no MassAssign — likely backbox or auxiliary inserts with direct object references (l73-l80). Lamp 32 not in MassAssign but has no callback either — possibly unused or backbox. Five flippers total: main L/R plus TopLeftFlipper (sol 12), TopRightFlipper (sol 13), RightFlipper2 (sol 14).

## Unresolved questions

- Is the I/O enumeration complete for every supported physical/controller variant?
- Which inferred VPX behaviors reflect real hardware, and which are table-script conveniences?
- Are all mechanism home states, sensors, motion constraints, and ball interactions documented?

## Sources

- `legacy.game.simp`: `games/simp.json` at the pinned migration revision.
