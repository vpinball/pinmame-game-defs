# Quicksilver

Coverage: **partial - source-derived recreation knowledge requiring validation**

## Overview

Legacy evidence identifies this candidate as Stern (1980). The information below is preserved for recreation work but is not automatically treated as validated physical-machine fact.

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

- `games/quicksilver.json#/switches/0._note`: vpmTimer.PulseSw 4 on each sw4_Spin event. Spinner with damping physics (sw4hit_Hit manages spin decay). VPX spinner object with animated BP_SpinR primitives.
- `games/quicksilver.json#/switches/1._note`: vpmTimer.PulseSw 5 on each sw5_Spin event. Spinner with damping physics (sw5hit_Hit manages spin decay). VPX spinner object with animated BP_SpinL primitives.
- `games/quicksilver.json#/switches/2._note`: vpmNudge.TiltSwitch=7. Sensitivity=5. TiltObj includes all 3 bumpers and both slingshots.
- `games/quicksilver.json#/switches/3._note`: vpmTimer.PulseSw(9) from Bumper1_Hit. Animated ring via BP_Bumper1_Ring.
- `games/quicksilver.json#/switches/4._note`: vpmTimer.PulseSw(10) from Bumper2_Hit. Animated ring via BP_Bumper2_Ring.
- `games/quicksilver.json#/switches/5._note`: vpmTimer.PulseSw(11) from Bumper3_Hit. Animated ring via BP_Bumper3_Ring.
- `games/quicksilver.json#/switches/6._note`: STHit 14 via StandupTarget class. VPX target sw14 with BM_sw14 primitive. Animated via Rothbauerw standup target system.
- `games/quicksilver.json#/switches/7._note`: STHit 15 via StandupTarget class. VPX target sw15 with BM_sw15 primitive.
- `games/quicksilver.json#/switches/8._note`: STHit 16 via StandupTarget class. VPX target sw16 with BM_sw16 primitive. Illuminated by lamp L54.
- `games/quicksilver.json#/switches/9._note`: Controller.Switch(17) on/off from sw17_hit/sw17_unhit. Wire trigger with animated BP_sw17 primitives.
- `games/quicksilver.json#/switches/10._note`: Controller.Switch(18) on/off from sw18_hit/sw18_unhit. Wire trigger with animated BP_sw18 primitives.
- `games/quicksilver.json#/switches/11._note`: Controller.Switch(19) on/off from sw19_hit/sw19_unhit. Wire trigger with animated BP_sw19 primitives.
- `games/quicksilver.json#/switches/12._note`: Dual-purpose switch. Fires from LeftSlingShot_Slingshot (PulseSw 20) AND from sw20 wire trigger (Controller.Switch(20) on/off). Wire trigger has BP_sw20 animation. Slingshot has sling correction physics (apophis SlingshotCorrection class).
- `games/quicksilver.json#/switches/13._note`: Dual-purpose switch. Fires from DTHit 21 (green drop target bank, first target) AND from RightSlingShot_Slingshot (PulseSw 21). Drop target uses Rothbauerw DTAnimate system with BM_sw21 primitive. Slingshot has sling correction physics. Illuminated by lamps L52, L62.
- `games/quicksilver.json#/switches/14._note`: DTHit 22 via DropTarget class. Green drop target bank, second target. BM_sw22 primitive. Illuminated by lamps L07, L23, L52, L62.
- `games/quicksilver.json#/switches/15._note`: DTHit 23 via DropTarget class. Green drop target bank, third target. BM_sw23 primitive. Illuminated by lamps L07, L23, L52, L62.
- `games/quicksilver.json#/switches/16._note`: DTHit 24 via DropTarget class. Green drop target bank, fourth target. BM_sw24 primitive. Illuminated by lamps L07, L23, L52, L62.
- `games/quicksilver.json#/switches/17._note`: STHit 25 via StandupTarget class. VPX target sw25 with BM_sw25 primitive.
- `games/quicksilver.json#/switches/18._note`: STHit 26 via StandupTarget class. VPX target sw26 with BM_sw26 primitive.
- `games/quicksilver.json#/switches/19._note`: STHit 27 via StandupTarget class. VPX target sw27 with BM_sw27 primitive.
- `games/quicksilver.json#/switches/20._note`: Controller.Switch(28) on/off from sw28_hit/sw28_unhit. Star trigger with BP_sw28 animation.
- `games/quicksilver.json#/switches/21._note`: Controller.Switch(29)=1 on hit, cleared by bsKicker solenoid (sol 9). Manual ball position tracking via KickerBall29 variable with timer-based wiggle prevention. Ball reflection disabled while in saucer. Physical saucer implementation by Sixtoe.
- `games/quicksilver.json#/switches/22._note`: DTHit 30 via DropTarget class. Yellow drop target bank, first target. DTBM_sw30 primitive.
- `games/quicksilver.json#/switches/23._note`: DTHit 31 via DropTarget class. Yellow drop target bank, second target. DTBM_sw31 primitive.
- `games/quicksilver.json#/switches/24._note`: DTHit 32 via DropTarget class. Yellow drop target bank, third target. DTBM_sw32 primitive.
- `games/quicksilver.json#/switches/25._note`: Controller.Switch(33) on/off from Drain_Hit/Drain_UnHit. bsTrough.InitSw 0,33,0,0,0,0,0,0 — single outhole switch. bsTrough.Balls=1 (single ball game). bsTrough.addball on drain hit.
- `games/quicksilver.json#/switches/26._note`: Controller.Switch(34) on/off from sw34_hit/sw34_unhit. Wire trigger with BP_sw34 animation.
- `games/quicksilver.json#/switches/27._note`: Controller.Switch(35) on/off from sw35_hit/sw35_unhit. Wire trigger with BP_sw35 animation.
- `games/quicksilver.json#/switches/28._note`: Controller.Switch(36) on/off from sw36_hit/sw36_unhit. Wire trigger with BP_sw36 animation.
- `games/quicksilver.json#/switches/29._note`: Controller.Switch(37) on/off from sw37_hit/sw37_unhit. Wire trigger with BP_sw37 animation.
- `games/quicksilver.json#/switches/30._note`: vpmTimer.PulseSw 38 from five separate VPX objects: sw38a, sw38b, sw38c, sw38d, sw38e. All pulse the same switch 38. Multiple rubber band segments that score on contact.
- `games/quicksilver.json#/switches/31._note`: Controller.Switch(39) on/off from sw39_hit/sw39_unhit. Star trigger with BP_sw39 animation.
- `games/quicksilver.json#/switches/32._note`: STHit 40 via StandupTarget class. VPX target sw40 with BM_sw40 primitive.
- `games/quicksilver.json#/coils/0._vbscript_callback`: GreenDropsUp
- `games/quicksilver.json#/coils/0._inferred_type`: drop_target_reset
- `games/quicksilver.json#/coils/0._note`: SolCallback(7)='GreenDropsUp'. Raises drop targets sw21-24 via DTRaise calls. Comment says 'Sol4 Center Drop Target Bank' but assigned to sol 7.
- `games/quicksilver.json#/coils/1._vbscript_callback`: YellowDropsUp
- `games/quicksilver.json#/coils/1._inferred_type`: drop_target_reset
- `games/quicksilver.json#/coils/1._note`: SolCallback(8)='YellowDropsUp'. Raises drop targets sw30-32 via DTRaise calls. Comment says 'Sol8 Right Drop Target Bank'.
- `games/quicksilver.json#/coils/2._vbscript_callback`: bsKicker
- `games/quicksilver.json#/coils/2._inferred_type`: ball_management
- `games/quicksilver.json#/coils/2._note`: SolCallback(9)='bsKicker'. Comment says 'Sol13 Kicker Hole'. Ejects ball from sw29 saucer via KickBall function (angle 150, vel 15, velz 5, zlift 20). Clears Controller.Switch(29) indirectly.
- `games/quicksilver.json#/coils/3._vbscript_callback`: bsTrough.SolOut
- `games/quicksilver.json#/coils/3._inferred_type`: ball_management
- `games/quicksilver.json#/coils/3._note`: SolCallback(10)='bsTrough.SolOut'. Comment says 'Sol14 Outhole, BallRelease'. Ejects ball from trough via BallRelease kicker (angle 90, force 5). Single-ball trough system.
- `games/quicksilver.json#/coils/4._vbscript_callback`: SolKnocker
- `games/quicksilver.json#/coils/4._vbscript_name`: SolKnocker
- `games/quicksilver.json#/coils/4._inferred_type`: knocker
- `games/quicksilver.json#/coils/4._note`: SolCallback(6)='SolKnocker' is COMMENTED OUT in the script. SolKnocker sub exists and calls KnockerSolenoid. Likely disabled for testing or sound reasons.
- `games/quicksilver.json#/coils/5._vbscript_callback`: SolRFlipper
- `games/quicksilver.json#/coils/5._inferred_type`: flipper
- `games/quicksilver.json#/coils/5._note`: SolCallback(sLRFlipper)='SolRFlipper'. sLRFlipper=16 from Stern.VBS framework. nFozzy flipper implementation (RF.Fire on enable, RotateToStart on disable). Includes reflip detection and live catch via CheckLiveCatch.
- `games/quicksilver.json#/coils/6._vbscript_callback`: SolLFlipper
- `games/quicksilver.json#/coils/6._inferred_type`: flipper
- `games/quicksilver.json#/coils/6._note`: SolCallback(sLLFlipper)='SolLFlipper'. sLLFlipper=18 from Stern.VBS framework. nFozzy flipper implementation (LF.Fire on enable, RotateToStart on disable). Includes reflip detection and live catch via CheckLiveCatch.
- `games/quicksilver.json#/coils/7._vbscript_callback`: FlipperRelay
- `games/quicksilver.json#/coils/7._inferred_type`: mechanism
- `games/quicksilver.json#/coils/7._note`: SolCallback(19)='FlipperRelay' is COMMENTED OUT. Comment says 'Sol19 sEnable'. This is the flipper enable relay for early Stern games.
- `games/quicksilver.json#/lamps/0._note`: vpmMapLights insert lamp. BL_L_L01 lightmap array.
- `games/quicksilver.json#/lamps/1._note`: vpmMapLights insert lamp. BL_L_L02 lightmap array.
- `games/quicksilver.json#/lamps/2._note`: vpmMapLights insert lamp. BL_L_L03 lightmap array.
- `games/quicksilver.json#/lamps/3._note`: vpmMapLights insert lamp. BL_L_L04 lightmap array.
- `games/quicksilver.json#/lamps/4._note`: vpmMapLights insert lamp. BL_L_L05 lightmap array.
- `games/quicksilver.json#/lamps/5._note`: vpmMapLights insert lamp. BL_L_L07 lightmap array. Illuminates area near drop targets sw22-24.
- `games/quicksilver.json#/lamps/6._note`: vpmMapLights insert lamp. BL_L_L08 lightmap array.
- `games/quicksilver.json#/lamps/7._note`: vpmMapLights insert lamp. BL_L_L09 lightmap array.
- `games/quicksilver.json#/lamps/8._note`: Backglass flasher lamp. Driven via LampCallback/UpdateMultipleLamps: Controller.Lamp(11) controls sa.state. Also has BL_L_L11 insert lightmap.
- `games/quicksilver.json#/lamps/9._note`: vpmMapLights insert lamp. BL_L_L12 lightmap array.
- `games/quicksilver.json#/lamps/10._note`: Backglass flasher lamp. Driven via LampCallback/UpdateMultipleLamps: Controller.Lamp(13) controls hstd.state.
- `games/quicksilver.json#/lamps/11._note`: vpmMapLights insert lamp. BL_L_L14 lightmap array.
- `games/quicksilver.json#/lamps/12._note`: vpmMapLights insert lamp. BL_L_L17 lightmap array.
- `games/quicksilver.json#/lamps/13._note`: vpmMapLights insert lamp. BL_L_L18 lightmap array.
- `games/quicksilver.json#/lamps/14._note`: vpmMapLights insert lamp. BL_L_L19 lightmap array.
- `games/quicksilver.json#/lamps/15._note`: vpmMapLights insert lamp. BL_L_L20 lightmap array.
- `games/quicksilver.json#/lamps/16._note`: vpmMapLights insert lamp. BL_L_L21 lightmap array.
- `games/quicksilver.json#/lamps/17._note`: vpmMapLights insert lamp. BL_L_L22 lightmap array.
- `games/quicksilver.json#/lamps/18._note`: vpmMapLights insert lamp. BL_L_L23 lightmap array. Illuminates area near drop targets sw22-24.
- `games/quicksilver.json#/lamps/19._note`: vpmMapLights insert lamp. BL_L_L24 lightmap array.
- `games/quicksilver.json#/lamps/20._note`: vpmMapLights insert lamp. BL_L_L28 lightmap array.
- `games/quicksilver.json#/lamps/21._note`: vpmMapLights insert lamp. BL_L_L30 lightmap array.
- `games/quicksilver.json#/lamps/22._note`: vpmMapLights insert lamp. BL_L_L31 lightmap array.
- `games/quicksilver.json#/lamps/23._note`: vpmMapLights insert lamp. BL_L_L33 lightmap array.
- `games/quicksilver.json#/lamps/24._note`: vpmMapLights insert lamp. BL_L_L34 lightmap array.
- `games/quicksilver.json#/lamps/25._note`: vpmMapLights insert lamp. BL_L_L35 lightmap array.
- `games/quicksilver.json#/lamps/26._note`: vpmMapLights insert lamp. BL_L_L36 lightmap array.
- `games/quicksilver.json#/lamps/27._note`: vpmMapLights insert lamp. BL_L_L37 lightmap array.
- `games/quicksilver.json#/lamps/28._note`: vpmMapLights insert lamp. BL_L_L38 lightmap array.
- `games/quicksilver.json#/lamps/29._note`: vpmMapLights insert lamp. BL_L_L39 lightmap array.
- `games/quicksilver.json#/lamps/30._note`: vpmMapLights insert lamp. BL_L_L40 lightmap array. Also illuminates Plas_Over plastic overlay.
- `games/quicksilver.json#/lamps/31._note`: vpmMapLights insert lamp. BL_L_L44 lightmap array.
- `games/quicksilver.json#/lamps/32._note`: Backglass flasher lamp. Driven via LampCallback/UpdateMultipleLamps: Controller.Lamp(45) controls go.state.
- `games/quicksilver.json#/lamps/33._note`: vpmMapLights insert lamp. BL_L_L46 lightmap array.
- `games/quicksilver.json#/lamps/34._note`: vpmMapLights insert lamp. BL_L_L47 lightmap array.
- `games/quicksilver.json#/lamps/35._note`: vpmMapLights insert lamp. BL_L_L49 lightmap array.
- `games/quicksilver.json#/lamps/36._note`: vpmMapLights insert lamp. BL_L_L50 lightmap array.
- `games/quicksilver.json#/lamps/37._note`: vpmMapLights insert lamp. BL_L_L51 lightmap array.
- `games/quicksilver.json#/lamps/38._note`: vpmMapLights insert lamp. BL_L_L52 lightmap array. Illuminates green drop target area (sw21-24).
- `games/quicksilver.json#/lamps/39._note`: vpmMapLights insert lamp. BL_L_L53 lightmap array.
- `games/quicksilver.json#/lamps/40._note`: vpmMapLights insert lamp. BL_L_L54 lightmap array. Illuminates standup target sw16 area.
- `games/quicksilver.json#/lamps/41._note`: vpmMapLights insert lamp. BL_L_L55 lightmap array.
- `games/quicksilver.json#/lamps/42._note`: vpmMapLights insert lamp. BL_L_L56 lightmap array.
- `games/quicksilver.json#/lamps/43._note`: vpmMapLights insert lamp. BL_L_L59 lightmap array.
- `games/quicksilver.json#/lamps/44._note`: vpmMapLights insert lamp. BL_L_L60 lightmap array.
- `games/quicksilver.json#/lamps/45._note`: Backglass flasher lamp. Driven via LampCallback/UpdateMultipleLamps: Controller.Lamp(61) controls tilt.state.
- `games/quicksilver.json#/lamps/46._note`: vpmMapLights insert lamp. BL_L_L62 lightmap array. Illuminates green drop target area (sw21-24).
- `games/quicksilver.json#/lamps/47._note`: Backglass flasher lamp. Driven via LampCallback/UpdateMultipleLamps: Controller.Lamp(63) controls ma.state.
- `games/quicksilver.json#/_source/confidence_notes`: High confidence extraction from VPW VBScript by MetaTed (with apophis, somatik, Sixtoe assistance). Platform detected as Stern pre-S11 era via LoadVPM '01560000','Stern.VBS',3.26. ROM name 'quicksic' from cGameName constant. Switches identified through multiple mechanisms: Controller.Switch() on/off calls for wire triggers and rollovers (sw17-20, sw28, sw29, sw33-37, sw39), vpmTimer.PulseSw for momentary switches (bumpers sw9-11, spinners sw4-5, slingshots sw20-21, scoring rubbers sw38), and custom STHit/DTHit class methods for standup targets (sw14-16, sw25-27, sw40) and drop targets (sw21-24, sw30-32). Trough is minimal single-ball cvpmBallStack design with bsTrough.InitSw using only sw33 as the outhole switch, with BallRelease kicker for eject (sol 10). No multi-ball trough stacking -- this is a 1980 Stern single-ball drain with bsTrough.Balls=1. Kicker/saucer at sw29 uses manual ball position tracking (KickerBall29 variable, timer-based wiggle prevention) with KickBall physics function for eject (sol 9 via bsKicker callback). Drop targets use elaborate Rothbauerw DTHit/DTAnimate class system with Controller.Switch(switchid)=1 on drop and =0 on raise. Green bank (sw21-24) reset by sol 7 (GreenDropsUp), yellow bank (sw30-32) reset by sol 8 (YellowDropsUp). Note sw20 is dual-purpose: fires from both LeftSlingShot_Slingshot event and sw20 wire trigger (Controller.Switch on/off). Similarly sw21 fires from RightSlingShot_Slingshot AND as green drop target 1. This likely reflects the actual Stern Quicksilver switch matrix where multiple playfield features share switch numbers. SolCallback(6)='SolKnocker' is commented out. SolCallback(19)='FlipperRelay' is commented out. Lamps use vpmMapLights with InsertLamps collection -- individual lamp IDs identified from VLM lightmap array names (BL_L_L01 through BL_L_L62). Five backglass flasher lamps handled via LampCallback/UpdateMultipleLamps: lamp 45 (Game Over), lamp 13 (High Score To Date), lamp 63 (Match), lamp 61 (Tilt), lamp 11 (Shoot Again) -- these drive VPX objects go, hstd, ma, tilt, sa respectively. GI is always on (UseGI=0, GI lights forced to state=1 at init). Flipper solenoids via Stern.VBS framework constants sLRFlipper and sLLFlipper (standard Stern values 16 and 18).

## Unresolved questions

- Is the I/O enumeration complete for every supported physical/controller variant?
- Which inferred VPX behaviors reflect real hardware, and which are table-script conveniences?
- Are all mechanism home states, sensors, motion constraints, and ball interactions documented?

## Sources

- `legacy.game.quicksilver`: `games/quicksilver.json` at the pinned migration revision.
