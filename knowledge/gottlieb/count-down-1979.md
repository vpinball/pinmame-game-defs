# Count-Down

Coverage: **partial - source-derived recreation knowledge requiring validation**

## Overview

Legacy evidence identifies this candidate as Gottlieb (1979). The information below is preserved for recreation work but is not automatically treated as validated physical-machine fact.

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

- `games/count-down.json#/switches/0._note`: vpmNudge.TiltSwitch = 4. Cabinet tilt switch.
- `games/count-down.json#/switches/1._note`: Controller.Switch(10) on/off. Wire rollover with AnimateWire BP_sw10. Located in upper left playfield area.
- `games/count-down.json#/switches/2._note`: Controller.Switch(11) on/off. Wire rollover with AnimateWire BP_sw11. Located in upper left playfield area near sw10.
- `games/count-down.json#/switches/3._note`: Controller.Switch(13) on/off. Wire rollover with AnimateWire BP_sw13. Located in right playfield area.
- `games/count-down.json#/switches/4._note`: Controller.Switch(14) on/off. Wire rollover with AnimateWire BP_sw14. Located in right playfield area near sw13.
- `games/count-down.json#/switches/5._inferred_type`: drop_target
- `games/count-down.json#/switches/5._note`: DTHit 20. Red drop target bank (sw20,21,23,24). Reset by sol 8 (ResetDropsRed).
- `games/count-down.json#/switches/6._inferred_type`: drop_target
- `games/count-down.json#/switches/6._note`: DTHit 21. Red drop target bank. Reset by sol 8 (ResetDropsRed).
- `games/count-down.json#/switches/7._inferred_type`: drop_target
- `games/count-down.json#/switches/7._note`: DTHit 23. Red drop target bank. Reset by sol 8 (ResetDropsRed).
- `games/count-down.json#/switches/8._inferred_type`: drop_target
- `games/count-down.json#/switches/8._note`: DTHit 24. Red drop target bank. Reset by sol 8 (ResetDropsRed).
- `games/count-down.json#/switches/9._inferred_type`: drop_target
- `games/count-down.json#/switches/9._note`: DTHit 30. Green drop target bank (sw30,31,33,34). Reset by sol 7 (ResetDropsGreen).
- `games/count-down.json#/switches/10._inferred_type`: drop_target
- `games/count-down.json#/switches/10._note`: DTHit 31. Green drop target bank. Reset by sol 7 (ResetDropsGreen).
- `games/count-down.json#/switches/11._inferred_type`: drop_target
- `games/count-down.json#/switches/11._note`: DTHit 33. Green drop target bank. Reset by sol 7 (ResetDropsGreen).
- `games/count-down.json#/switches/12._inferred_type`: drop_target
- `games/count-down.json#/switches/12._note`: DTHit 34. Green drop target bank. Reset by sol 7 (ResetDropsGreen).
- `games/count-down.json#/switches/13._note`: Controller.Switch(40) on/off. Wire rollover with AnimateWire BP_sw40. Center playfield area. VLM LM_LI_L12_sw40 suggests illuminated by lamp 12.
- `games/count-down.json#/switches/14._inferred_type`: saucer
- `games/count-down.json#/switches/14._note`: Controller.Switch(41)=1 on hit. Ball captured by KickerBall41 reference. Released by sol 6 (SolSaucerRelease) via KickBall helper. Animated kick arm (BP_PkickarmR).
- `games/count-down.json#/switches/15._note`: Controller.Switch(43) on/off. Wire rollover with AnimateWire BP_sw43.
- `games/count-down.json#/switches/16._note`: Controller.Switch(44) on/off. Wire rollover with AnimateWire BP_sw44.
- `games/count-down.json#/switches/17._note`: Controller.Switch(50) on/off. Wire rollover with AnimateWire BP_sw50. VLM LM_LI_L11_sw50 suggests illuminated by lamp 11.
- `games/count-down.json#/switches/18._inferred_type`: bumper
- `games/count-down.json#/switches/18._note`: vpmTimer.PulseSw 51 in Bumper1_Hit. Single pop bumper. Also used as vpmNudge.TiltObj target. Has animated ring and skirt tilt.
- `games/count-down.json#/switches/19._inferred_type`: slingshot
- `games/count-down.json#/switches/19._note`: PulseSw 53 from 14 different VPX trigger objects: sw53a-sw53h (rubber bands — upper top/bottom, mid, lower pairs), sw53i/sw53i_LC/sw53i_LL (left slingshot variants), sw53j/sw53j_RC/sw53j_RL (right slingshot variants). All side rubber contacts and both slingshots share this single switch number. Gottlieb System 1 used shared switch matrix positions for similar playfield elements.
- `games/count-down.json#/switches/20._inferred_type`: drop_target
- `games/count-down.json#/switches/20._note`: DTHit 60. Yellow drop target bank (sw60,61,63,64). Reset triggered by lamp 17 via LampCallback (ResetDropsYellow).
- `games/count-down.json#/switches/21._inferred_type`: drop_target
- `games/count-down.json#/switches/21._note`: DTHit 61. Yellow drop target bank. Reset triggered by lamp 17 via LampCallback.
- `games/count-down.json#/switches/22._inferred_type`: drop_target
- `games/count-down.json#/switches/22._note`: DTHit 63. Yellow drop target bank. Reset triggered by lamp 17 via LampCallback.
- `games/count-down.json#/switches/23._inferred_type`: drop_target
- `games/count-down.json#/switches/23._note`: DTHit 64. Yellow drop target bank. Reset triggered by lamp 17 via LampCallback.
- `games/count-down.json#/switches/24._note`: Controller.Switch(66)=1 set in Drain_Hit. Cleared by sol 1 (SolBallRelease). Single-ball game — ball sits in Drain kicker between plays. No multi-ball trough. Set to 1 at table init.
- `games/count-down.json#/switches/25._inferred_type`: drop_target
- `games/count-down.json#/switches/25._note`: DTHit 70. Blue drop target bank (sw70,71,73,74). Reset triggered by lamp 18 via LampCallback (ResetDropsBlue).
- `games/count-down.json#/switches/26._inferred_type`: drop_target
- `games/count-down.json#/switches/26._note`: DTHit 71. Blue drop target bank. Reset triggered by lamp 18 via LampCallback.
- `games/count-down.json#/switches/27._inferred_type`: drop_target
- `games/count-down.json#/switches/27._note`: DTHit 73. Blue drop target bank. Reset triggered by lamp 18 via LampCallback.
- `games/count-down.json#/switches/28._inferred_type`: drop_target
- `games/count-down.json#/switches/28._note`: DTHit 74. Blue drop target bank. Reset triggered by lamp 18 via LampCallback.
- `games/count-down.json#/coils/0._vbscript_callback`: SolBallRelease
- `games/count-down.json#/coils/0._inferred_type`: ball_management
- `games/count-down.json#/coils/0._note`: Kicks ball from Drain kicker (angle 57, speed 20). Clears Controller.Switch(66). Single-ball trough — no multi-switch stack.
- `games/count-down.json#/coils/1._vbscript_callback`: vpmsolsound SoundFX("fx_knocker",DOFKnocker),
- `games/count-down.json#/coils/1._inferred_type`: knocker
- `games/count-down.json#/coils/1._note`: Cabinet knocker solenoid. Sound-only callback in VBS.
- `games/count-down.json#/coils/2._vbscript_callback`: If PlayChimes = 1 Then VpmSolSound"10pts",
- `games/count-down.json#/coils/2._inferred_type`: chime
- `games/count-down.json#/coils/2._note`: 10-point scoring chime. Conditionally plays sound based on PlayChimes user option (default off). Gottlieb System 1 used electromechanical chimes for scoring sounds.
- `games/count-down.json#/coils/3._vbscript_callback`: If PlayChimes = 1 Then VpmSolSound"100chime",
- `games/count-down.json#/coils/3._inferred_type`: chime
- `games/count-down.json#/coils/3._note`: 100-point scoring chime. Conditionally plays sound based on PlayChimes user option.
- `games/count-down.json#/coils/4._vbscript_callback`: If PlayChimes = 1 Then VpmSolSound"1000chime",
- `games/count-down.json#/coils/4._inferred_type`: chime
- `games/count-down.json#/coils/4._note`: 1000-point scoring chime. Conditionally plays sound based on PlayChimes user option.
- `games/count-down.json#/coils/5._vbscript_callback`: SolSaucerRelease
- `games/count-down.json#/coils/5._inferred_type`: ball_management
- `games/count-down.json#/coils/5._note`: Releases ball from saucer (sw41) via KickBall helper (angle 170, vel 10, velz 5, zlift 10). Clears Controller.Switch(41). Triggers kick arm animation.
- `games/count-down.json#/coils/6._vbscript_callback`: ResetDropsGreen
- `games/count-down.json#/coils/6._inferred_type`: drop_target_reset
- `games/count-down.json#/coils/6._note`: Resets green drop target bank (sw30,31,33,34). DTRaise calls for all 4 targets. Updates DTShadows visibility (indices 4-7).
- `games/count-down.json#/coils/7._vbscript_callback`: ResetDropsRed
- `games/count-down.json#/coils/7._inferred_type`: drop_target_reset
- `games/count-down.json#/coils/7._note`: Resets red drop target bank (sw20,21,23,24). DTRaise calls for all 4 targets. Updates DTShadows visibility (indices 0-3).
- `games/count-down.json#/coils/8._vbscript_callback`: vpmNudge.SolGameOn
- `games/count-down.json#/coils/8._inferred_type`: mechanism
- `games/count-down.json#/coils/8._note`: Standard Game On relay. Enables nudge/tilt detection via vpmNudge framework.
- `games/count-down.json#/lamps/0._note`: Lamp 1 in UpdateLamps. Controller.Lamp(1) checked in VR mode for backglass Ball In Play indicator.
- `games/count-down.json#/lamps/1._note`: Lamp 2 in UpdateLamps. Has secondary object li2a (Lampm). Controller.Lamp(2) checked in VR mode for VR_BGTilt.
- `games/count-down.json#/lamps/2._note`: Lamp 3 in UpdateLamps. Controller.Lamp(3) checked in VR mode for VR_BGHS.
- `games/count-down.json#/lamps/3._note`: Lamp 4 in UpdateLamps. Has additional objects li4a and li4b (Lampm). VR mode checks l4.state for VR_BGSA visibility.
- `games/count-down.json#/lamps/4._note`: Lamp 5 in UpdateLamps. VLM BL_LI_L5 illuminates parts, PegPlasticSlingL1C, playfield, Rubber10 objects.
- `games/count-down.json#/lamps/5._note`: Lamp 6 in UpdateLamps. VLM BL_LI_L6 illuminates parts, PegPlasticSlingL1C, playfield, Rubber10, RubberLSling objects.
- `games/count-down.json#/lamps/6._note`: Lamp 7 in UpdateLamps. VLM BL_LI_L7 illuminates playfield area.
- `games/count-down.json#/lamps/7._note`: Lamp 8 in UpdateLamps. VLM BL_LI_L8 illuminates overlay, parts, playfield, sw61, sw63 areas.
- `games/count-down.json#/lamps/8._note`: Lamp 9 in UpdateLamps. VLM BL_LI_L9 illuminates playfield area.
- `games/count-down.json#/lamps/9._note`: Lamp 10 in UpdateLamps. VLM BL_LI_L10 illuminates playfield area.
- `games/count-down.json#/lamps/10._note`: Lamp 11 in UpdateLamps. VLM BL_LI_L11 illuminates playfield and sw50 rollover area.
- `games/count-down.json#/lamps/11._note`: Lamp 12 in UpdateLamps. VLM BL_LI_L12 illuminates playfield and sw40 rollover area.
- `games/count-down.json#/lamps/12._note`: Lamp 13 in UpdateLamps. VLM BL_LI_L13 illuminates parts and playfield.
- `games/count-down.json#/lamps/13._note`: Lamp 14 in UpdateLamps. VLM BL_LI_L14 illuminates parts, playfield, and Rubber7 area.
- `games/count-down.json#/lamps/14._note`: Lamp 15 in UpdateLamps. VLM BL_LI_L15 illuminates parts and playfield.
- `games/count-down.json#/lamps/15._note`: Lamp 16 in UpdateLamps. VLM BL_LI_L16 illuminates parts and playfield.
- `games/count-down.json#/lamps/16._note`: NOT a physical lamp — used as a signal. Controller.Lamp(17) monitored by LampCallback (UpdateMultipleLamps). When lamp 17 transitions to on, ResetDropsYellow is called to reset yellow drop targets (sw60,61,63,64). Gottlieb System 1 lamp-as-coil pattern.
- `games/count-down.json#/lamps/17._note`: NOT a physical lamp — used as a signal. Controller.Lamp(18) monitored by LampCallback (UpdateMultipleLamps). When lamp 18 transitions to on, ResetDropsBlue is called to reset blue drop targets (sw70,71,73,74). Gottlieb System 1 lamp-as-coil pattern.
- `games/count-down.json#/lamps/18._note`: Lamp 19 in UpdateLamps. VLM BL_LI_L19 illuminates playfield area.
- `games/count-down.json#/lamps/19._note`: Lamp 20 in UpdateLamps. VLM BL_LI_L20 illuminates playfield area.
- `games/count-down.json#/lamps/20._note`: Lamp 21 in UpdateLamps. VLM BL_LI_L21 illuminates playfield area.
- `games/count-down.json#/lamps/21._note`: Lamp 22 in UpdateLamps. VLM BL_LI_L22 illuminates playfield area.
- `games/count-down.json#/lamps/22._note`: Lamp 23 in UpdateLamps. VLM BL_LI_L23 illuminates LFlip, LFlipU, playfield, RFlip, RFlipU areas — likely center playfield near flippers.
- `games/count-down.json#/lamps/23._note`: Lamp 24 in UpdateLamps. VLM BL_LI_L24 illuminates LFlipU and playfield — near left upper flipper.
- `games/count-down.json#/lamps/24._note`: Lamp 25 in UpdateLamps. VLM BL_LI_L25 illuminates playfield and RFlipU — near right upper flipper.
- `games/count-down.json#/lamps/25._note`: Lamp 26 in UpdateLamps. VLM BL_LI_L26 illuminates playfield area.
- `games/count-down.json#/lamps/26._note`: Lamp 27 in UpdateLamps. VLM BL_LI_L27 illuminates playfield area.
- `games/count-down.json#/lamps/27._note`: Lamp 28 in UpdateLamps. VLM BL_LI_L28 illuminates playfield area.
- `games/count-down.json#/lamps/28._note`: Lamp 29 in UpdateLamps. VLM BL_LI_L29 illuminates playfield area.
- `games/count-down.json#/lamps/29._note`: Lamp 30 in UpdateLamps. VLM BL_LI_L30 illuminates playfield area.
- `games/count-down.json#/lamps/30._note`: Lamp 31 in UpdateLamps. VLM BL_LI_L31 illuminates playfield area.
- `games/count-down.json#/lamps/31._note`: Lamp 32 in UpdateLamps. VLM BL_LI_L32 illuminates playfield area.
- `games/count-down.json#/lamps/32._note`: Lamp 33 in UpdateLamps. VLM BL_LI_L33 illuminates playfield area.
- `games/count-down.json#/lamps/33._note`: Lamp 35 in UpdateLamps. VLM BL_LI_L35 illuminates overlay, parts, PegPlasticSlingR1C, playfield, Rubber9, sw74 — near right sling area.
- `games/count-down.json#/lamps/34._note`: Lamp 36 in UpdateLamps. VLM BL_LI_L36 illuminates overlay, parts, PegPlasticSlingR1C, PegPlasticSlingRC, playfield, Rubber9, RubberRSling — right slingshot area.
- `games/count-down.json#/_source/confidence_notes`: High confidence on switches, coils, and lamps. Platform identified as Gottlieb System 1 via LoadVPM call loading 'gts1.vbs'. ROM name is 'countdwn' from Const cGameName. This is a single-ball game (tnob=1, lob=0) with a simple drain/kicker trough — no cvpmTrough framework used. The drain is a single VPX kicker object ('Drain') that sets Controller.Switch(66)=1 on hit. Ball release solenoid (sol 1) kicks the ball from Drain and clears sw66. No multi-ball trough stack — the ball sits in the Drain kicker between plays. Switches found via Controller.Switch on/off pairs (_Hit/_UnHit subs for rollovers sw10,11,13,14,40,43,44,50), PulseSw calls (sw51 bumper, sw53 slingshots/rubbers), DTHit calls for 16 drop targets in 4 banks of 4 (Red: 20,21,23,24; Green: 30,31,33,34; Yellow: 60,61,63,64; Blue: 70,71,73,74), and Controller.Switch direct set for saucer sw41. Drop target reset solenoids: sol 7 (Green bank) and sol 8 (Red bank). Yellow and Blue resets are triggered by LampCallback watching Controller.Lamp(17) and Controller.Lamp(18) — these are lamp-driven resets, not direct solenoid-driven. Saucer at sw41 uses KickBall helper, released by sol 6. GI is not ROM-controlled — uses ball-presence detection (GIUpdate checks GetBalls count). Flipper solenoid IDs use framework constants sLRFlipper/sLLFlipper/sURFlipper/sULFlipper from gts1.vbs — exact IDs are platform-defined, not in this table script. Four flippers total: LeftFlipper, RightFlipper, LeftFlipper1 (upper left), RightFlipper1 (upper right). Sol 17 is vpmNudge.SolGameOn. Sols 3,4,5 are chime solenoids (10pt, 100pt, 1000pt) conditionally played based on PlayChimes user option. Lamps mapped via JP's Lamp Fading system (LampTimer) with explicit Lamp(N, object) calls in UpdateLamps sub — 33 lamp IDs identified (1-16, 19-33, 35-36). Lamp 1 = Game Over, Lamp 2 = Tilt, Lamp 3 = High Game, Lamp 4 = Same Player Shoots Again (with multi-object li4a/li4b). Lamps 17 and 18 are used as drop target reset triggers via LampCallback, not as physical lights. VPX light objects use 'li' prefix (li1, li2, li3... li36). VLM baked lighting system uses LM_LI_L{N} arrays for raytraced insert lighting per lamp. No Lampz.MassAssign — uses vpmMapLights AllLamps instead. TiltSwitch=4 per vpmNudge configuration.

## Unresolved questions

- Is the I/O enumeration complete for every supported physical/controller variant?
- Which inferred VPX behaviors reflect real hardware, and which are table-script conveniences?
- Are all mechanism home states, sensors, motion constraints, and ball interactions documented?

## Sources

- `legacy.game.count-down`: `games/count-down.json` at the pinned migration revision.
