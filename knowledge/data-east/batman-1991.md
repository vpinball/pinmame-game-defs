# Batman

Coverage: **partial - source-derived recreation knowledge requiring validation**

## Overview

Legacy evidence identifies this candidate as Data East (1991). The information below is preserved for recreation work but is not automatically treated as validated physical-machine fact.

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

- `games/batman.json#/switches/0._note`: vpmNudge.TiltSwitch = 1
- `games/batman.json#/switches/1._note`: bsTrough.EntrySw = 10. Drain_Hit triggers sound.
- `games/batman.json#/switches/2._note`: bsTrough.InitSwitches Array(13,12,11) — sw11 is position 3 (nearest eject). Size=3.
- `games/batman.json#/switches/3._note`: bsTrough.InitSwitches Array(13,12,11) — sw12 is position 2.
- `games/batman.json#/switches/4._note`: bsTrough.InitSwitches Array(13,12,11) — sw13 is position 1 (nearest drain).
- `games/batman.json#/switches/5._note`: Sw14_Hit/UnHit tracks BallInPlungerLane variable. plungerIM.switch 14.
- `games/batman.json#/switches/6._note`: Controller.Switch(17) on/off. Part of top rollover lanes.
- `games/batman.json#/switches/7._note`: Controller.Switch(18) on/off. Part of top rollover lanes.
- `games/batman.json#/switches/8._note`: Controller.Switch(19) on/off. Part of top rollover lanes.
- `games/batman.json#/switches/9._note`: Controller.Switch(21) on/off.
- `games/batman.json#/switches/10._note`: Controller.Switch(22) on/off.
- `games/batman.json#/switches/11._note`: Controller.Switch(23) on/off.
- `games/batman.json#/switches/12._note`: Controller.Switch(24) on/off.
- `games/batman.json#/switches/13._note`: Controller.Switch(28) on/off. Comment says 'Center Ramp'.
- `games/batman.json#/switches/14._note`: Controller.Switch(29) on/off. Comment says 'Center Ramp Exit'.
- `games/batman.json#/switches/15._note`: PulseSw 33. Left bank of 3 standup targets with animation.
- `games/batman.json#/switches/16._note`: PulseSw 34. Left bank of 3 standup targets with animation.
- `games/batman.json#/switches/17._note`: PulseSw 35. Left bank of 3 standup targets with animation.
- `games/batman.json#/switches/18._note`: Controller.Switch(36) on/off. Joker face target — left eye. Animated gate with psw36 primitive.
- `games/batman.json#/switches/19._note`: Controller.Switch(37) on/off. Joker face target — right eye. Animated gate with psw37 primitive.
- `games/batman.json#/switches/20._note`: Controller.Switch(38) on/off. Joker face target — mouth. Animated gate with psw38 primitive.
- `games/batman.json#/switches/21._note`: Controller.Switch(39)=1 on hit, cleared by ScoopKickL solenoid 3.
- `games/batman.json#/switches/22._note`: PulseSw 41. Right bank of 3 standup targets with animation.
- `games/batman.json#/switches/23._note`: PulseSw 42. Right bank of 3 standup targets with animation.
- `games/batman.json#/switches/24._note`: PulseSw 43. Right bank of 3 standup targets with animation.
- `games/batman.json#/switches/25._note`: PulseSw 47. Fired from LeftSlingShot_Slingshot event.
- `games/batman.json#/switches/26._note`: PulseSw 48. Fired from RightSlingShot_Slingshot event.
- `games/batman.json#/switches/27._note`: PulseSw 49. Target on the bar mechanism.
- `games/batman.json#/switches/28._note`: cvpmMech.AddSw 50,0,0 — mechanism position switch at home position. Set to 0 on init.
- `games/batman.json#/switches/29._note`: cvpmMech.AddSw 51,47,49 — mechanism position switch at steps 47-49. Set to 1 on init.
- `games/batman.json#/switches/30._note`: Controller.Switch(52)=1 on hit, cleared by ScoopKickR solenoid 6.
- `games/batman.json#/switches/31._note`: Controller.Switch(53)=1 set by ball tracking code when ball is above right scoop (z < -60). Cleared by ScoopKickR solenoid 6.
- `games/batman.json#/switches/32._note`: PulseSw 54. Bumper1B_Hit.
- `games/batman.json#/switches/33._note`: PulseSw 55. Bumper3B_Hit.
- `games/batman.json#/switches/34._note`: PulseSw 56. Bumper2B_Hit.
- `games/batman.json#/coils/0._vbscript_callback`: bsTrough.SolIn
- `games/batman.json#/coils/0._inferred_type`: ball_management
- `games/batman.json#/coils/0._note`: 6-ball lockout. bsTrough.SolIn.
- `games/batman.json#/coils/1._vbscript_callback`: bsTrough.SolOut
- `games/batman.json#/coils/1._inferred_type`: ball_management
- `games/batman.json#/coils/1._note`: Ball eject from trough. bsTrough.SolOut via BallRelease kicker.
- `games/batman.json#/coils/2._vbscript_callback`: ScoopKickL
- `games/batman.json#/coils/2._inferred_type`: ball_management
- `games/batman.json#/coils/2._note`: Kicks ball out of left scoop (sw39). sw39.Kick 0,85,1.56.
- `games/batman.json#/coils/3._vbscript_callback`: SolAutoPlungerIM
- `games/batman.json#/coils/3._inferred_type`: ball_management
- `games/batman.json#/coils/3._note`: Impulse plunger auto-fire. plungerIM.AutoFire.
- `games/batman.json#/coils/4._vbscript_callback`: ScoopKickR
- `games/batman.json#/coils/4._inferred_type`: ball_management
- `games/batman.json#/coils/4._note`: Kicks ball out of right scoop (sw52). sw52.Kick 0,40,1.56. Also clears sw52 and sw53.
- `games/batman.json#/coils/5._vbscript_callback`: Solknocker
- `games/batman.json#/coils/5._inferred_type`: knocker
- `games/batman.json#/coils/5._note`: Cabinet knocker solenoid.
- `games/batman.json#/coils/6._vbscript_callback`: Sol9
- `games/batman.json#/coils/6._inferred_type`: flasher
- `games/batman.json#/coils/6._note`: FlashLamp x4 (2 backbox + 2 pf). Sets lamp 109.
- `games/batman.json#/coils/7._vbscript_callback`: Sol11
- `games/batman.json#/coils/7._inferred_type`: mechanism
- `games/batman.json#/coils/7._note`: GI Relay — INVERTED. When enabled, GI turns OFF (cuts circuit). Sets lamp 111. DE-era inverted GI behavior.
- `games/batman.json#/coils/8._vbscript_callback`: Sol12
- `games/batman.json#/coils/8._inferred_type`: flasher
- `games/batman.json#/coils/8._note`: FlashLamp x4 (1 pf + 3 backbox). Sets lamp 112.
- `games/batman.json#/coils/9._vbscript_callback`: Sol13
- `games/batman.json#/coils/9._inferred_type`: flasher
- `games/batman.json#/coils/9._note`: FlashLamp x4 (2 pf + 2 backbox). Sets lamp 113.
- `games/batman.json#/coils/10._vbscript_callback`: Sol14
- `games/batman.json#/coils/10._inferred_type`: flasher
- `games/batman.json#/coils/10._note`: FlashLamp x4 (1 pf + 3 backbox). Sets lamp 114.
- `games/batman.json#/coils/11._vbscript_callback`: cvpmMech (mBar.Sol1 = 16)
- `games/batman.json#/coils/11._inferred_type`: mechanism
- `games/batman.json#/coils/11._note`: Bar motor driven by cvpmMech framework. vpmMechOneSol + vpmMechReverse + vpmMechNonLinear. 50 steps, length 130. Controls bar toy position and sw49 target availability. Not in SolCallback — consumed by framework.
- `games/batman.json#/coils/12._vbscript_callback`: SolDiv
- `games/batman.json#/coils/12._inferred_type`: diverter
- `games/batman.json#/coils/12._note`: Controls RampDiverter and RampDiverter2 drop state.
- `games/batman.json#/coils/13._vbscript_callback`: Sol25
- `games/batman.json#/coils/13._inferred_type`: flasher
- `games/batman.json#/coils/13._note`: Flashlamp X4 (3 pf + backbox). Sets lamp 125.
- `games/batman.json#/coils/14._vbscript_callback`: Sol26
- `games/batman.json#/coils/14._inferred_type`: flasher
- `games/batman.json#/coils/14._note`: Flashlamp X4 (1 pf + 2 ramp + 1 backbox). Sets lamp 126.
- `games/batman.json#/coils/15._vbscript_callback`: Sol27
- `games/batman.json#/coils/15._inferred_type`: flasher
- `games/batman.json#/coils/15._note`: Flashlamp X4 (2 pf + 2 backbox). Sets lamp 127.
- `games/batman.json#/coils/16._vbscript_callback`: Sol28
- `games/batman.json#/coils/16._inferred_type`: flasher
- `games/batman.json#/coils/16._note`: Flashlamp X4 (2 pf + 2 backbox). Sets lamp 128.
- `games/batman.json#/coils/17._vbscript_callback`: SetLamp 129,
- `games/batman.json#/coils/17._inferred_type`: flasher
- `games/batman.json#/coils/17._note`: Flashlamp X4 (4 pf). Direct SetLamp callback for lamp 129. Flash129 sub drives 4 dome flasher objects.
- `games/batman.json#/coils/18._vbscript_callback`: Sol30
- `games/batman.json#/coils/18._inferred_type`: flasher
- `games/batman.json#/coils/18._note`: Flashlamp X4 (3 pf + 1 backbox). Sets lamp 130. Has bulb filament and clear bulb image/material swaps.
- `games/batman.json#/coils/19._vbscript_callback`: Sol31
- `games/batman.json#/coils/19._inferred_type`: flasher
- `games/batman.json#/coils/19._note`: Flashlamp X4 (3 pf + 1 backbox). Sets lamp 131.
- `games/batman.json#/coils/20._vbscript_callback`: Flash132
- `games/batman.json#/coils/20._inferred_type`: flasher
- `games/batman.json#/coils/20._note`: Flashlamp X4 (2 bat + 2 backbox). Custom Flash132 sub with museumflash fading. Lamp 132 (museum).
- `games/batman.json#/coils/21._vbscript_callback`: SolRFlipper
- `games/batman.json#/coils/21._inferred_type`: flipper
- `games/batman.json#/coils/21._note`: nFozzy flipper implementation. RF.Fire on enable.
- `games/batman.json#/coils/22._vbscript_callback`: SolLFlipper
- `games/batman.json#/coils/22._inferred_type`: flipper
- `games/batman.json#/coils/22._note`: nFozzy flipper implementation. LF.Fire on enable.
- `games/batman.json#/lamps/16._note`: Also has flasher primitives L17f
- `games/batman.json#/lamps/17._note`: Also has flasher primitives L18f
- `games/batman.json#/lamps/18._note`: Also has flasher primitives L19f
- `games/batman.json#/lamps/22._note`: Also has flasher primitives l23f
- `games/batman.json#/lamps/24._note`: Flasher lamp for Sol25. Callback Flash25. No MassAssign VPX light objects — uses callback-only Lampz integration.
- `games/batman.json#/lamps/25._note`: Flasher lamp for Sol26. Callback Flash26. No MassAssign VPX light objects — uses callback-only Lampz integration.
- `games/batman.json#/lamps/26._note`: Flasher lamp for Sol27. Callback Flash27. No MassAssign VPX light objects — uses callback-only Lampz integration.
- `games/batman.json#/lamps/27._note`: Flasher lamp for Sol28. Callback Flash28. No MassAssign VPX light objects — uses callback-only Lampz integration.
- `games/batman.json#/lamps/28._note`: Flasher lamp for Sol29. Callback Flash29. No MassAssign VPX light objects — uses callback-only Lampz integration.
- `games/batman.json#/lamps/35._note`: Also has l36b, l36Fb, l36Fb2 objects
- `games/batman.json#/lamps/36._note`: Also has l37b, l37Fb objects
- `games/batman.json#/lamps/43._note`: ImageSwap on pBumperCap1. Also has BumperL_Flasher_a, Bumberhalolb/Bumberhalol.
- `games/batman.json#/lamps/44._note`: ImageSwap on pBumperCap3. Also has BumperB_Flasher_a, Bumberhalobb/Bumberhalob.
- `games/batman.json#/lamps/45._note`: ImageSwap on pBumperCap2. Also has Bumberhalorb/Bumberhalor.
- `games/batman.json#/lamps/48._note`: Also has l49f flasher primitive
- `games/batman.json#/lamps/59._note`: Mapped from solenoid 9. Also has Flasher9a.
- `games/batman.json#/lamps/60._note`: GI controlled via Sol11 relay. Inverted — sol enabled = GI off. aGiLights array.
- `games/batman.json#/lamps/61._note`: Mapped from solenoid 12.
- `games/batman.json#/lamps/62._note`: Mapped from solenoid 14.
- `games/batman.json#/lamps/63._note`: Mapped from solenoid 25. Also has FlasherL2b.
- `games/batman.json#/lamps/64._note`: Mapped from solenoid 26. Also has FlasherLight2b, FlasherLight2c.
- `games/batman.json#/lamps/65._note`: Mapped from solenoid 27.
- `games/batman.json#/lamps/66._note`: Mapped from solenoid 28.
- `games/batman.json#/lamps/67._note`: Mapped from solenoid 29. Callback Flash129 drives 4 dome flasher fade sequences.
- `games/batman.json#/lamps/68._note`: Mapped from solenoid 30. Also has Flasher6a, Flasher6c. Bulb filament and material swap effects.
- `games/batman.json#/lamps/69._note`: Mapped from solenoid 31. Also has FlasherLight7b/c/d/e.
- `games/batman.json#/lamps/70._note`: Mapped from solenoid 32. Custom Flash132 sub with museum fading. Objects commented out — uses callback only.
- `games/batman.json#/_source/confidence_notes`: High confidence on switches/coils. No Const sw* definitions — switches identified from _Hit/_UnHit subs, Controller.Switch() calls, and PulseSw calls. Lamp IDs from Lampz.MassAssign() calls. Trough is 3-ball cvpmTrough with switches 11-13 and entry switch 10. Solenoid 16 (Bar Motor) handled via cvpmMech — not in SolCallback but consumed by framework. Solenoids 5, 7, 10 unused. Solenoids 15-21 commented out — handled by VPX physics (bumpers, slingshots). Flasher solenoids use SetLamp with 100+ lamp IDs for Lampz integration. GI Relay (sol 11) is inverted — enabled cuts GI circuit. Sw36/37/38 are Joker face switches (eyes and mouth) using Controller.Switch on/off (not PulseSw). Sw50/51 are bar mechanism position switches set via cvpmMech. Sw53 set by ball tracking code when ball is above right scoop.

## Unresolved questions

- Is the I/O enumeration complete for every supported physical/controller variant?
- Which inferred VPX behaviors reflect real hardware, and which are table-script conveniences?
- Are all mechanism home states, sensors, motion constraints, and ball interactions documented?

## Sources

- `legacy.game.batman`: `games/batman.json` at the pinned migration revision.
