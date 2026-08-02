# Radical!

Coverage: **partial - source-derived recreation knowledge requiring validation**

## Overview

Legacy evidence identifies this candidate as Bally (1990). The information below is preserved for recreation work but is not automatically treated as validated physical-machine fact.

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

- `games/rad.json#/switches/0._note`: cvpmBallStack.InitSw first position. Drain_Hit adds ball to bsTrough.
- `games/rad.json#/switches/1._note`: cvpmBallStack.InitSw second position
- `games/rad.json#/switches/2._note`: cvpmBallStack.InitSw third position
- `games/rad.json#/switches/3._note`: Controller.Switch rollover
- `games/rad.json#/switches/4._note`: Controller.Switch rollover
- `games/rad.json#/switches/5._note`: cvpmBallStack bsTP switch. Prototype-only feature, not in latest ROMs. Ball enters via sw16a_Hit, ejected after 2500ms delay.
- `games/rad.json#/switches/6._note`: PulseSw 17 from Spinner2_Spin
- `games/rad.json#/switches/7._note`: Controller.Switch rollover
- `games/rad.json#/switches/8._note`: Controller.Switch rollover
- `games/rad.json#/switches/9._note`: Set by SolRampDiv sub — Controller.Switch(20) toggled when diverter changes position. Not a physical switch on playfield.
- `games/rad.json#/switches/10._note`: cvpmDropTarget dtBankM. Sound-only _Hit sub.
- `games/rad.json#/switches/11._note`: cvpmDropTarget dtBankM. Sound-only _Hit sub.
- `games/rad.json#/switches/12._note`: cvpmDropTarget dtBankM. Sound-only _Hit sub.
- `games/rad.json#/switches/13._note`: Controller.Switch rollover
- `games/rad.json#/switches/14._note`: PulseSw 28 with random bounce multiplier
- `games/rad.json#/switches/15._note`: PulseSw 29 from Spinner1_Spin
- `games/rad.json#/switches/16._note`: cvpmDropTarget dtBankT. Sound-only _Hit sub.
- `games/rad.json#/switches/17._note`: cvpmDropTarget dtBankT. Sound-only _Hit sub.
- `games/rad.json#/switches/18._note`: cvpmDropTarget dtBankT. Sound-only _Hit sub.
- `games/rad.json#/switches/19._note`: Controller.Switch rollover
- `games/rad.json#/switches/20._note`: Controller.Switch rollover
- `games/rad.json#/switches/21._note`: cvpmVLock bsLock second position. Ball kicked by sw39k.
- `games/rad.json#/switches/22._note`: cvpmVLock bsLock first position. Ball kicked by sw40k.
- `games/rad.json#/switches/23._note`: PulseSw 43 with random bounce multiplier
- `games/rad.json#/switches/24._note`: PulseSw 44 with random bounce multiplier
- `games/rad.json#/switches/25._note`: Controller.Switch rollover
- `games/rad.json#/switches/26._note`: Controller.Switch rollover
- `games/rad.json#/switches/27._note`: Controller.Switch rollover
- `games/rad.json#/switches/28._note`: PulseSw 49 from RightSlingShot1_Slingshot. Prototype-only, disabled when DisableUpperSling=1.
- `games/rad.json#/switches/29._note`: PulseSw 50 from Bumper2_Hit
- `games/rad.json#/switches/30._note`: Controller.Switch rollover. Also used as impulse plunger switch (plungerIM.switch 51).
- `games/rad.json#/switches/31._note`: PulseSw 52 from Bumper1_Hit
- `games/rad.json#/switches/32._note`: PulseSw 53 from Bumper4_Hit
- `games/rad.json#/switches/33._note`: PulseSw 54 from Bumper3_Hit
- `games/rad.json#/switches/34._note`: PulseSw 55 from LeftSlingShot_Slingshot sub
- `games/rad.json#/switches/35._note`: PulseSw 56 from RightSlingShot_Slingshot sub
- `games/rad.json#/coils/0._vbscript_callback`: bsTrough.SolIn
- `games/rad.json#/coils/0._inferred_type`: ball_management
- `games/rad.json#/coils/0._note`: Handles ball entry into trough stack
- `games/rad.json#/coils/1._vbscript_callback`: bsTrough.SolOut
- `games/rad.json#/coils/1._inferred_type`: ball_management
- `games/rad.json#/coils/1._note`: Kicks ball from BallRelease kicker at power 80, angle 6
- `games/rad.json#/coils/2._vbscript_callback`: bsTP.SolOut
- `games/rad.json#/coils/2._inferred_type`: kicker
- `games/rad.json#/coils/2._note`: Prototype-only. Not used in latest ROMs. Kicks from sw16 kicker at power 55.
- `games/rad.json#/coils/3._vbscript_callback`: dtBankT.SolDropUp
- `games/rad.json#/coils/3._inferred_type`: drop_target_reset
- `games/rad.json#/coils/3._note`: Resets top 3-bank drop targets (sw30, sw31, sw32)
- `games/rad.json#/coils/4._vbscript_callback`: VpmSolSound SoundFX("fx_knocker",DOFKnocker),
- `games/rad.json#/coils/4._inferred_type`: knocker
- `games/rad.json#/coils/5._vbscript_callback`: dtBankM.SolDropUp
- `games/rad.json#/coils/5._inferred_type`: drop_target_reset
- `games/rad.json#/coils/5._note`: Resets middle 3-bank drop targets (sw22, sw23, sw24)
- `games/rad.json#/coils/6._vbscript_callback`: SolRampDiv
- `games/rad.json#/coils/6._inferred_type`: diverter
- `games/rad.json#/coils/6._note`: Toggles ramp diverter position and Controller.Switch(20) feedback
- `games/rad.json#/coils/7._vbscript_callback`: bsLock.SolExit
- `games/rad.json#/coils/7._inferred_type`: kicker
- `games/rad.json#/coils/7._note`: cvpmVLock exit. Releases locked balls from sw40/sw39 positions via sw40k/sw39k kickers.
- `games/rad.json#/coils/8._vbscript_callback`: FlashPurpleMiddleRight
- `games/rad.json#/coils/8._note`: Flasher solenoid. Originally SetLamp 90.
- `games/rad.json#/coils/9._vbscript_callback`: SolGI
- `games/rad.json#/coils/9._inferred_type`: gi
- `games/rad.json#/coils/9._note`: Controls general illumination. Inverted logic: enabled=GiOFF, disabled=GiON.
- `games/rad.json#/coils/10._vbscript_callback`: vpmSolToggleWall RightDiverter2,RightDiverter1,"fx_diverter",
- `games/rad.json#/coils/10._inferred_type`: diverter
- `games/rad.json#/coils/10._note`: Toggles right diverter walls
- `games/rad.json#/coils/11._vbscript_callback`: SolKickBack
- `games/rad.json#/coils/11._inferred_type`: kicker
- `games/rad.json#/coils/11._note`: Fires impulse plunger (plungerIM.AutoFire) for kickback
- `games/rad.json#/coils/12._vbscript_callback`: SetLamp 116,
- `games/rad.json#/coils/12._note`: Flasher driven as lamp 116. Mapped to f16 VPX light in UpdateLamps.
- `games/rad.json#/coils/13._vbscript_callback`: vpmNudge.SolGameOn
- `games/rad.json#/coils/13._inferred_type`: system
- `games/rad.json#/coils/14._vbscript_callback`: FlashPurpleLeftBottom
- `games/rad.json#/coils/14._note`: Flasher solenoid. Originally SetLamp 125.
- `games/rad.json#/coils/15._vbscript_callback`: FlashGreenLeftBottom
- `games/rad.json#/coils/15._note`: Flasher solenoid. Originally SetLamp 126.
- `games/rad.json#/coils/16._vbscript_callback`: FlashPurpleMiddleLeft
- `games/rad.json#/coils/16._note`: Flasher solenoid. Originally SetLamp 127.
- `games/rad.json#/coils/17._vbscript_callback`: FlashGreenLeftTop
- `games/rad.json#/coils/17._note`: Flasher solenoid. Originally SetLamp 128.
- `games/rad.json#/coils/18._vbscript_callback`: FlashWhiteBack
- `games/rad.json#/coils/18._note`: Flasher solenoid. Originally SetLamp 129.
- `games/rad.json#/coils/19._vbscript_callback`: FlashPurpleMiddleTop
- `games/rad.json#/coils/19._note`: Flasher solenoid. Originally SetLamp 130.
- `games/rad.json#/coils/20._vbscript_callback`: FlashGreenTop
- `games/rad.json#/coils/20._note`: Flasher solenoid. Originally SetLamp 131.
- `games/rad.json#/coils/21._vbscript_callback`: FlashGreenRight
- `games/rad.json#/coils/21._note`: Flasher solenoid. Originally SetLamp 132.
- `games/rad.json#/lamps/0._note`: Playfield insert
- `games/rad.json#/lamps/1._note`: Playfield insert
- `games/rad.json#/lamps/2._note`: Playfield insert
- `games/rad.json#/lamps/3._note`: Playfield insert
- `games/rad.json#/lamps/4._note`: Playfield insert
- `games/rad.json#/lamps/5._note`: Playfield insert
- `games/rad.json#/lamps/6._note`: Playfield insert
- `games/rad.json#/lamps/7._note`: Playfield insert
- `games/rad.json#/lamps/8._note`: Dual-mapped playfield insert
- `games/rad.json#/lamps/9._note`: Dual-mapped playfield insert
- `games/rad.json#/lamps/10._note`: Dual-mapped playfield insert
- `games/rad.json#/lamps/11._note`: Dual-mapped playfield insert
- `games/rad.json#/lamps/12._note`: Dual-mapped playfield insert
- `games/rad.json#/lamps/13._note`: Dual-mapped playfield insert
- `games/rad.json#/lamps/14._note`: Dual-mapped playfield insert
- `games/rad.json#/lamps/15._note`: Playfield insert
- `games/rad.json#/lamps/16._note`: Dual-mapped playfield insert
- `games/rad.json#/lamps/17._note`: Dual-mapped playfield insert
- `games/rad.json#/lamps/18._note`: Dual-mapped playfield insert
- `games/rad.json#/lamps/19._note`: Dual-mapped playfield insert
- `games/rad.json#/lamps/20._note`: Dual-mapped playfield insert
- `games/rad.json#/lamps/21._note`: Dual-mapped playfield insert
- `games/rad.json#/lamps/22._note`: Dual-mapped playfield insert
- `games/rad.json#/lamps/23._note`: Playfield insert
- `games/rad.json#/lamps/24._note`: Playfield insert
- `games/rad.json#/lamps/25._note`: Playfield insert
- `games/rad.json#/lamps/26._note`: Playfield insert
- `games/rad.json#/lamps/27._note`: Playfield insert
- `games/rad.json#/lamps/28._note`: Playfield insert
- `games/rad.json#/lamps/29._note`: Playfield insert
- `games/rad.json#/lamps/30._note`: Playfield insert
- `games/rad.json#/lamps/31._note`: Playfield insert
- `games/rad.json#/lamps/32._note`: Playfield insert
- `games/rad.json#/lamps/33._note`: Playfield insert
- `games/rad.json#/lamps/34._note`: Playfield insert
- `games/rad.json#/lamps/35._note`: Dual-mapped playfield insert
- `games/rad.json#/lamps/36._note`: Playfield insert
- `games/rad.json#/lamps/37._note`: Playfield insert
- `games/rad.json#/lamps/38._note`: Playfield insert
- `games/rad.json#/lamps/39._note`: Playfield insert
- `games/rad.json#/lamps/40._note`: Playfield insert
- `games/rad.json#/lamps/41._note`: Playfield insert
- `games/rad.json#/lamps/42._note`: Playfield insert
- `games/rad.json#/lamps/43._note`: Playfield insert
- `games/rad.json#/lamps/44._note`: Playfield insert
- `games/rad.json#/lamps/45._note`: Playfield insert
- `games/rad.json#/lamps/46._note`: Playfield insert
- `games/rad.json#/lamps/47._note`: Playfield insert
- `games/rad.json#/lamps/48._note`: Playfield insert
- `games/rad.json#/lamps/49._note`: Playfield insert
- `games/rad.json#/lamps/50._note`: Playfield insert
- `games/rad.json#/lamps/51._note`: Playfield insert
- `games/rad.json#/lamps/52._note`: Playfield insert
- `games/rad.json#/lamps/53._note`: Playfield insert
- `games/rad.json#/lamps/54._note`: Playfield insert
- `games/rad.json#/lamps/55._note`: Playfield insert
- `games/rad.json#/lamps/56._note`: Backglass lamp (Flash sub). Desktop-only VPX light, always drives bg1 flasher.
- `games/rad.json#/lamps/57._note`: Backglass lamp (Flash sub). Desktop-only VPX light, always drives bg2 flasher.
- `games/rad.json#/lamps/58._note`: Backglass lamp (Flash sub). Desktop-only VPX light, always drives bg3 flasher.
- `games/rad.json#/lamps/59._note`: Backglass lamp (Flash sub). Desktop-only VPX light, always drives bg4 flasher.
- `games/rad.json#/lamps/60._note`: Backglass lamp (Flash sub). Desktop-only VPX light, always drives bg5 flasher.
- `games/rad.json#/lamps/61._note`: Backglass lamp (Flash sub). Desktop-only VPX light, always drives bg6 flasher.
- `games/rad.json#/lamps/62._note`: Playfield insert
- `games/rad.json#/lamps/63._note`: Playfield insert
- `games/rad.json#/lamps/64._note`: Ramp flasher on front left. Driven by SolCallback(16) via SetLamp 116.
- `games/rad.json#/_source/confidence_notes`: High confidence on switches/coils. No Const sw* definitions in script — switches identified from _Hit/_UnHit subs, Controller.Switch() calls, PulseSw calls, and cvpmBallStack/cvpmVLock/cvpmDropTarget init. Platform is System 11 (S11.VBS). This is the prototype playfield version with additional upper slingshot (sw49) and top eject hole (sw16/sol3) not present on production games. Trough uses cvpmBallStack with 3 switches (10,11,12) and 2 balls. Lock uses cvpmVLock with switches 39,40. Drop targets in two banks: middle (22,23,24) and top (30,31,32). Flashers are driven via solenoid callbacks (9,16,25-32) with custom flash subs. Ramp diverter (sol7) toggles switch 20 as feedback. GI controlled via sol10 (inverted — enabled=off). Flipper solenoids use S11.VBS framework constants sLRFlipper/sLLFlipper. Lamps 57-62 are backglass lamps using Flash sub.

## Unresolved questions

- Is the I/O enumeration complete for every supported physical/controller variant?
- Which inferred VPX behaviors reflect real hardware, and which are table-script conveniences?
- Are all mechanism home states, sensors, motion constraints, and ball interactions documented?

## Sources

- `legacy.game.rad`: `games/rad.json` at the pinned migration revision.
