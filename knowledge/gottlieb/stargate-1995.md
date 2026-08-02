# Stargate

Coverage: **partial - source-derived recreation knowledge requiring validation**

## Overview

Legacy evidence identifies this candidate as Gottlieb (1995). The information below is preserved for recreation work but is not automatically treated as validated physical-machine fact.

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

- `games/stargate.json#/switches/0._note`: Controller.Switch(5) set by RightMagnaSave keypress and TournamentTimer_Timer auto-set at startup.
- `games/stargate.json#/switches/1._note`: Controller.Switch(6) set by TournamentTimer_Timer at startup. Const swFrontDoor = 6.
- `games/stargate.json#/switches/2._note`: PulseSw 10. Bumper1_Hit. Sound S02_BumperBottom. Has skirt and ring animation.
- `games/stargate.json#/switches/3._note`: PulseSw 11. Bumper2_Hit. Sound S01_Bumper_Top. Has skirt and ring animation.
- `games/stargate.json#/switches/4._note`: PulseSw 12. LeftSlingShot_Slingshot event. Has 3-step sling animation.
- `games/stargate.json#/switches/5._note`: PulseSw 13. RightSlingShot_Slingshot event. Has 3-step sling animation.
- `games/stargate.json#/switches/6._note`: KTHit 14 via Rothbauerw KickingTarget class. sw14col_hit triggers KTKick. Kickback solenoid 5 (commented out).
- `games/stargate.json#/switches/7._note`: KTHit 15 via KickingTarget class. sw15col_hit triggers KTKick. Kickback solenoid 6 (commented out).
- `games/stargate.json#/switches/8._note`: KTHit 16 via KickingTarget class. sw16col_hit triggers KTKick. Kickback solenoid 7 (commented out).
- `games/stargate.json#/switches/9._note`: DTHit 17. Part of 3-bank left drop targets (17/27/37). Reset by sol 17 LeftDropUp.
- `games/stargate.json#/switches/10._note`: Controller.Switch(21) set by GliderTimer when GliderY <= GliderYMin + 2. Indicates glider is at home/forward position.
- `games/stargate.json#/switches/11._note`: PulseSw 22. sw22_Hit. Has standup target animation via STHit (not used directly - uses direct PulseSw instead).
- `games/stargate.json#/switches/12._note`: Controller.Switch(23) on/off. sw23_Hit captures ball. BotPop (sol 11) kicks ball out with KickBall velocity z=60.
- `games/stargate.json#/switches/13._note`: Controller.Switch(24) on/off. Drain_Hit/UnHit. Init: Controller.Switch(24)=1. SolTrough (sol 29) kicks ball from Drain.
- `games/stargate.json#/switches/14._note`: Controller.Switch(25) on/off. sw25_Hit/UnHit. SolLeftPlunge (sol 8) kicks ball out with sw25.Kick 0,40.
- `games/stargate.json#/switches/15._note`: DTHit 26. Part of 2-bank top drop targets (26/36). Reset by sol 18 TopDropUp.
- `games/stargate.json#/switches/16._note`: DTHit 27. Part of 3-bank left drop targets (17/27/37). Reset by sol 17 LeftDropUp.
- `games/stargate.json#/switches/17._note`: Controller.Switch(30) set by GliderTimer when GliderRot > GliderRotMax - 1. Indicates glider LR motor at right limit.
- `games/stargate.json#/switches/18._note`: Controller.Switch(31) on/off via SW31_Hit/UnHit wire trigger. Ball presence checked on PlungerKey release. plungerIM.InitImpulseP swPlunger references this via GTS3 framework.
- `games/stargate.json#/switches/19._note`: STHit 32. Standup target with animation via UpdateStandupTargets.
- `games/stargate.json#/switches/20._note`: Controller.Switch(33) on/off. sw33_Hit captures KickerBall33. VukTopPop (sol 12) kicks ball with KickBall velocity z=40.
- `games/stargate.json#/switches/21._note`: Controller.Switch(34) set by swTrough3_Hit/UnHit. Init: Controller.Switch(34)=1. Indicates ball is in last trough position (ready for release).
- `games/stargate.json#/switches/22._note`: DTHit 35. Single drop target on right side. Reset by sol 19 RightDropUp. Trip by sol 20 RightDropTrip.
- `games/stargate.json#/switches/23._note`: DTHit 36. Part of 2-bank top drop targets (26/36). Reset by sol 18 TopDropUp.
- `games/stargate.json#/switches/24._note`: DTHit 37. Part of 3-bank left drop targets (17/27/37). Reset by sol 17 LeftDropUp.
- `games/stargate.json#/switches/25._note`: Controller.Switch(80) on/off. sw80_Hit captures KickerBall80. LeftPop (sol 10) kicks ball with KickBall velocity z=40.
- `games/stargate.json#/switches/26._note`: Controller.Switch(81) set by LeftFlipperKey in KeyDown/KeyUp handlers.
- `games/stargate.json#/switches/27._note`: Controller.Switch(82) set by RightFlipperKey in KeyDown/KeyUp handlers. Also triggers RightFlipper1.RotateToStart on KeyUp.
- `games/stargate.json#/switches/28._note`: PulseSw 90. sw90_Hit.
- `games/stargate.json#/switches/29._note`: PulseSw 91. sw91_Hit. Ball enters pyramid subway. Sound popperball_pyramide.
- `games/stargate.json#/switches/30._note`: PulseSw 100. sw100_Hit.
- `games/stargate.json#/switches/31._note`: Controller.Switch(101) set by SolDiv (sol 13). Set to 1 when diverter opens, 0 when closes. Feedback switch for ROM.
- `games/stargate.json#/switches/32._note`: Controller.Switch(102) set by SolPyramid (sol 16) via delayed timer (500ms). Set to -1 (true) when open, 0 when closed.
- `games/stargate.json#/switches/33._note`: PulseSw 110. sw110_Hit.
- `games/stargate.json#/switches/34._note`: Controller.Switch(111) on/off. SW111_Hit/UnHit with wire animation.
- `games/stargate.json#/switches/35._note`: Controller.Switch(112) on/off. SW112_Hit/UnHit with wire animation. Triggers leftInlaneSpeedLimit physics correction.
- `games/stargate.json#/switches/36._note`: Controller.Switch(113) on/off. SW113_Hit/UnHit with wire animation. Triggers rightInlaneSpeedLimit physics correction.
- `games/stargate.json#/switches/37._note`: Controller.Switch(114) on/off. SW114_Hit/UnHit with wire animation.
- `games/stargate.json#/switches/38._note`: Controller.Switch(115) on/off. SW115_Hit/UnHit with wire animation.
- `games/stargate.json#/switches/39._note`: STHit 116. Collidable only when LeftGuardianDown=True. SolPivL (sol 14) makes sw116 non-collidable when pivot opens.
- `games/stargate.json#/switches/40._note`: STHit 117. Collidable only when RightGuardianDown=True. SolPivR (sol 15) makes sw117 non-collidable when pivot opens.
- `games/stargate.json#/coils/0._vbscript_callback`: (commented out)
- `games/stargate.json#/coils/0._inferred_type`: bumper
- `games/stargate.json#/coils/0._note`: SolCallback(1) commented out -- 'Bumper 1'. Handled by VPX physics.
- `games/stargate.json#/coils/1._vbscript_callback`: (commented out)
- `games/stargate.json#/coils/1._inferred_type`: bumper
- `games/stargate.json#/coils/1._note`: SolCallback(2) commented out -- 'Bumper 2'. Handled by VPX physics.
- `games/stargate.json#/coils/2._vbscript_callback`: (commented out)
- `games/stargate.json#/coils/2._inferred_type`: slingshot
- `games/stargate.json#/coils/2._note`: SolCallback(3) commented out -- 'Left SlingShot'. Handled by VPX physics.
- `games/stargate.json#/coils/3._vbscript_callback`: (commented out)
- `games/stargate.json#/coils/3._inferred_type`: slingshot
- `games/stargate.json#/coils/3._note`: SolCallback(4) commented out -- 'Right SlingShot'. Handled by VPX physics.
- `games/stargate.json#/coils/4._vbscript_callback`: (commented out)
- `games/stargate.json#/coils/4._inferred_type`: kicker
- `games/stargate.json#/coils/4._note`: SolCallback(5) commented out -- 'sw14 kickback'. Kicking target kickback for left target.
- `games/stargate.json#/coils/5._vbscript_callback`: (commented out)
- `games/stargate.json#/coils/5._inferred_type`: kicker
- `games/stargate.json#/coils/5._note`: SolCallback(6) commented out -- 'sw15 kickback'. Kicking target kickback for center target.
- `games/stargate.json#/coils/6._vbscript_callback`: (commented out)
- `games/stargate.json#/coils/6._inferred_type`: kicker
- `games/stargate.json#/coils/6._note`: SolCallback(7) commented out -- 'sw16 kickback'. Kicking target kickback for right target.
- `games/stargate.json#/coils/7._vbscript_callback`: SolLeftPlunge
- `games/stargate.json#/coils/7._inferred_type`: ball_management
- `games/stargate.json#/coils/7._note`: Kicks ball from sw25 kicker hole. sw25.Kick 0,40. Sound S08_LowerLeftKicker.
- `games/stargate.json#/coils/8._vbscript_callback`: SolAutoFire
- `games/stargate.json#/coils/8._inferred_type`: ball_management
- `games/stargate.json#/coils/8._note`: Impulse plunger auto-fire. PlungerIM.AutoFire. Animates APFlipper. Sound S09_ShooterLaneKicker.
- `games/stargate.json#/coils/9._vbscript_callback`: LeftPop
- `games/stargate.json#/coils/9._inferred_type`: ball_management
- `games/stargate.json#/coils/9._note`: Kicks ball from left VUK (sw80). KickBall velocity z=40.
- `games/stargate.json#/coils/10._vbscript_callback`: BotPop
- `games/stargate.json#/coils/10._inferred_type`: ball_management
- `games/stargate.json#/coils/10._note`: Kicks ball from center VUK (sw23). KickBall velocity z=60.
- `games/stargate.json#/coils/11._vbscript_callback`: VukTopPop
- `games/stargate.json#/coils/11._inferred_type`: ball_management
- `games/stargate.json#/coils/11._note`: Kicks ball from right VUK (sw33). KickBall velocity z=40.
- `games/stargate.json#/coils/12._vbscript_callback`: SolDiv
- `games/stargate.json#/coils/12._inferred_type`: diverter
- `games/stargate.json#/coils/12._note`: Controls diverter gate via Flipper1 VPX flipper object. Sets Controller.Switch(101) for position feedback. Sound S13_LowerLeftBallGateOpen/Close.
- `games/stargate.json#/coils/13._vbscript_callback`: SolPivL
- `games/stargate.json#/coils/13._inferred_type`: mechanism
- `games/stargate.json#/coils/13._note`: Opens/closes left guardian pivot. Sets sw116/sw116a collidable state. Uses LeftFlipper2 VPX flipper. TrapTriggerL_Hit auto-opens if ball stuck behind. Sound S14_LeftPivotTargetOpen/Close.
- `games/stargate.json#/coils/14._vbscript_callback`: SolPivR
- `games/stargate.json#/coils/14._inferred_type`: mechanism
- `games/stargate.json#/coils/14._note`: Opens/closes right guardian pivot. Sets sw117/sw117a collidable state. Uses RightFlipper2 VPX flipper. TrapTriggerR_Hit auto-opens if ball stuck behind. Sound S15_RightPivotTargetOpen/Close.
- `games/stargate.json#/coils/15._vbscript_callback`: SolPyramid
- `games/stargate.json#/coils/15._inferred_type`: mechanism
- `games/stargate.json#/coils/15._note`: Opens/closes pyramid mechanism. Uses LeftFlipper1 VPX flipper for animation. Sets Controller.Switch(102) via 500ms delayed timer. Sound S16_TopPyramidOpen/Close.
- `games/stargate.json#/coils/16._vbscript_callback`: LeftDropUp
- `games/stargate.json#/coils/16._inferred_type`: drop_target_reset
- `games/stargate.json#/coils/16._note`: Resets 3-bank left drop targets (sw17/sw27/sw37). DTRaise 17,27,37. Sound S17_3BankDropTargetReset.
- `games/stargate.json#/coils/17._vbscript_callback`: TopDropUp
- `games/stargate.json#/coils/17._inferred_type`: drop_target_reset
- `games/stargate.json#/coils/17._note`: Resets 2-bank top drop targets (sw26/sw36). DTRaise 26,36. Sound S18_2BankDropTargetReset.
- `games/stargate.json#/coils/18._vbscript_callback`: RightDropUp
- `games/stargate.json#/coils/18._inferred_type`: drop_target_reset
- `games/stargate.json#/coils/18._note`: Resets single right drop target (sw35). DTRaise 35. Sound S19_RollOverTargetReset.
- `games/stargate.json#/coils/19._vbscript_callback`: RightDropTrip
- `games/stargate.json#/coils/19._inferred_type`: drop_target_trip
- `games/stargate.json#/coils/19._note`: Trips/drops single right drop target (sw35). DTDrop 35. Sound S20_RollOverTargetTrip.
- `games/stargate.json#/coils/20._vbscript_callback`: (commented out)
- `games/stargate.json#/coils/20._inferred_type`: unused
- `games/stargate.json#/coils/20._note`: SolCallback(21) commented out -- 'Not Used'.
- `games/stargate.json#/coils/21._vbscript_callback`: SolBGRopeLights
- `games/stargate.json#/coils/21._inferred_type`: mechanism
- `games/stargate.json#/coils/21._note`: Controls backglass rope lights. VR mode only: toggles BGTube.state. No playfield effect in desktop mode.
- `games/stargate.json#/coils/22._vbscript_callback`: SolGlid1
- `games/stargate.json#/coils/22._inferred_type`: mechanism
- `games/stargate.json#/coils/22._note`: Controls glider left-right oscillation motor. Sets GliderLROn flag. GliderTimer drives animation and sets sw30 (right limit position). Sound Glidercraft.
- `games/stargate.json#/coils/23._vbscript_callback`: SolGlid2
- `games/stargate.json#/coils/23._inferred_type`: mechanism
- `games/stargate.json#/coils/23._note`: Controls glider forward-backward motor. Sets GliderFROn flag. GliderTimer drives animation and sets sw21 (home position). Sound Glidercraft_retract.
- `games/stargate.json#/coils/24._vbscript_callback`: (commented out)
- `games/stargate.json#/coils/24._inferred_type`: unused
- `games/stargate.json#/coils/24._note`: SolCallback(25) commented out -- 'Not Used'.
- `games/stargate.json#/coils/25._vbscript_callback`: SolBBGI
- `games/stargate.json#/coils/25._inferred_type`: mechanism
- `games/stargate.json#/coils/25._note`: Backbox GI control. VR mode only effect (BGLights state toggle, currently commented out).
- `games/stargate.json#/coils/26._vbscript_callback`: (commented out)
- `games/stargate.json#/coils/26._inferred_type`: mechanism
- `games/stargate.json#/coils/26._note`: SolCallback(27) commented out -- 'Ticket dispenser'. Not implemented.
- `games/stargate.json#/coils/27._vbscript_callback`: SolRelease
- `games/stargate.json#/coils/27._inferred_type`: ball_management
- `games/stargate.json#/coils/27._note`: Ejects ball from trough position 1 (swTrough1). swTrough1.kick 57,10. Sound S28_BallRelease.
- `games/stargate.json#/coils/28._vbscript_callback`: SolTrough
- `games/stargate.json#/coils/28._inferred_type`: ball_management
- `games/stargate.json#/coils/28._note`: Kicks ball from Drain into trough. Drain.kick 57,20. Separate from ball release -- feeds trough from outhole.
- `games/stargate.json#/coils/29._vbscript_callback`: SolKnocker
- `games/stargate.json#/coils/29._inferred_type`: knocker
- `games/stargate.json#/coils/29._note`: Cabinet knocker solenoid. Sound S30_Knocker.
- `games/stargate.json#/coils/30._vbscript_callback`: GIState
- `games/stargate.json#/coils/30._inferred_type`: mechanism
- `games/stargate.json#/coils/30._note`: Playfield GI control. INVERTED: Not Enabled = GI ON (gilvl=1), Enabled = GI OFF (gilvl=0). Iterates GI collection setting bulb.State. Sound Flash_Relay.
- `games/stargate.json#/coils/31._vbscript_callback`: (commented out)
- `games/stargate.json#/coils/31._inferred_type`: mechanism
- `games/stargate.json#/coils/31._note`: SolCallback(32) commented out -- 'Game Over Relay'. Standard GTS3 game over relay, not implemented in VBS.
- `games/stargate.json#/lamps/0._note`: From BL_L_L0 lightmap array. Illuminates LF, RF, Parts, Playfield, UnderPF.
- `games/stargate.json#/lamps/1._note`: From BL_L_L5 lightmap array. Illuminates RSling1 area.
- `games/stargate.json#/lamps/2._note`: From BL_L_L6 lightmap array. Illuminates RSling area.
- `games/stargate.json#/lamps/3._note`: From BL_L_L7 lightmap array. Illuminates RSling area.
- `games/stargate.json#/lamps/4._note`: From BL_L_L11 lightmap array. Illuminates left slingshot area (LSling, Layer2).
- `games/stargate.json#/lamps/5._note`: From BL_L_L12 lightmap array. Illuminates left slingshot area.
- `games/stargate.json#/lamps/6._note`: From BL_L_L13 lightmap array. Illuminates right slingshot area (RSling).
- `games/stargate.json#/lamps/7._note`: From BL_L_L14 lightmap array.
- `games/stargate.json#/lamps/8._note`: From BL_L_L15 lightmap array. Illuminates Bumper1 skirt, DT_sw37 area.
- `games/stargate.json#/lamps/9._note`: From BL_L_L16 lightmap array.
- `games/stargate.json#/lamps/10._note`: From BL_L_L17 lightmap array. Illuminates Bumper1 skirt, DT_sw26 area.
- `games/stargate.json#/lamps/11._note`: From BL_L_L21 lightmap array.
- `games/stargate.json#/lamps/12._note`: From BL_L_L22 lightmap array.
- `games/stargate.json#/lamps/13._note`: From BL_L_L23 lightmap array.
- `games/stargate.json#/lamps/14._note`: From BL_L_L24 lightmap array.
- `games/stargate.json#/lamps/15._note`: From BL_L_L25 lightmap array. Illuminates Layer1, RF1/RF1U area.
- `games/stargate.json#/lamps/16._note`: From BL_L_L26 lightmap array. Illuminates Layer1, RF1U area.
- `games/stargate.json#/lamps/17._note`: From BL_L_L27 lightmap array. Illuminates DT_sw35, Layer1 area.
- `games/stargate.json#/lamps/18._note`: From BL_L_L32 lightmap array.
- `games/stargate.json#/lamps/19._note`: From BL_L_L33 lightmap array. Illuminates DT_sw26 area.
- `games/stargate.json#/lamps/20._note`: From BL_L_L34 lightmap array. Illuminates DT_sw26, DT_sw36 area.
- `games/stargate.json#/lamps/21._note`: From BL_L_L35 lightmap array. Illuminates RF1U area.
- `games/stargate.json#/lamps/22._note`: From BL_L_L36 lightmap array.
- `games/stargate.json#/lamps/23._note`: From BL_L_L37 lightmap array.
- `games/stargate.json#/lamps/24._note`: From BL_L_L41 lightmap array. Illuminates Bumper1 ring and skirt.
- `games/stargate.json#/lamps/25._note`: From BL_L_L42 lightmap array. Illuminates Bumper2 ring, skirt, Plastics.
- `games/stargate.json#/lamps/26._note`: From BL_L_L43 lightmap array. Illuminates Bumper1 ring/skirt, Layer2, SideBlades.
- `games/stargate.json#/lamps/27._note`: From BL_L_L44 lightmap array. Illuminates Bumper2 ring/skirt, GuardianL, KT_sw14.
- `games/stargate.json#/lamps/28._note`: From BL_L_L45 lightmap array. Illuminates DT_sw36 area.
- `games/stargate.json#/lamps/29._note`: From BL_L_L46 lightmap array. Illuminates DT_sw36, ST_sw32 area.
- `games/stargate.json#/lamps/30._note`: From BL_L_L47 lightmap array. Illuminates ST_sw32 area.
- `games/stargate.json#/lamps/31._note`: From BL_L_L55 lightmap array. Illuminates ST_sw32 area.
- `games/stargate.json#/lamps/32._note`: From BL_L_L56 lightmap array.
- `games/stargate.json#/lamps/33._note`: From BL_L_L57 lightmap array. Illuminates KT_sw15 area.
- `games/stargate.json#/lamps/34._note`: From BL_L_L65 lightmap array. Illuminates GuardianR area.
- `games/stargate.json#/lamps/35._note`: From BL_L_L66 lightmap array. Illuminates GuardianR area.
- `games/stargate.json#/lamps/36._note`: From BL_L_L67 lightmap array. Illuminates GuardianR area.
- `games/stargate.json#/lamps/37._note`: From BL_L_L71 lightmap array.
- `games/stargate.json#/lamps/38._note`: From BL_L_L72 lightmap array.
- `games/stargate.json#/lamps/39._note`: From BL_L_L73 lightmap array.
- `games/stargate.json#/lamps/40._note`: From BL_L_L74 lightmap array.
- `games/stargate.json#/lamps/41._note`: From BL_L_L75 lightmap array.
- `games/stargate.json#/lamps/42._note`: From BL_L_L76 lightmap array. Illuminates KT_sw16 area.
- `games/stargate.json#/lamps/43._note`: From BL_L_L77 lightmap array.
- `games/stargate.json#/lamps/44._note`: From BL_L_L81 lightmap array. Illuminates left slingshot area.
- `games/stargate.json#/lamps/45._note`: From BL_L_L82 lightmap array. Illuminates LF (left flipper), LSling area.
- `games/stargate.json#/lamps/46._note`: From BL_L_L83 lightmap array. Illuminates LF (left flipper) area.
- `games/stargate.json#/lamps/47._note`: From BL_L_L84 lightmap array. Illuminates RF (right flipper) area.
- `games/stargate.json#/lamps/48._note`: From BL_L_L85 lightmap array. Illuminates RF (right flipper), RSling area.
- `games/stargate.json#/lamps/49._note`: From BL_L_L86 lightmap array. Illuminates RSling1 area.
- `games/stargate.json#/lamps/50._note`: From BL_L_L87 lightmap array.
- `games/stargate.json#/lamps/51._note`: From BL_BC_L90 backglass lightmap array. Illuminates Glass, Metal, VRRR.
- `games/stargate.json#/lamps/52._note`: From BL_BC_L92 backglass lightmap array. Illuminates Metal, VRRR.
- `games/stargate.json#/lamps/53._note`: From BL_BC_L112 backglass lightmap array. Illuminates Metal, VRRR.
- `games/stargate.json#/lamps/54._note`: L120_animate sets f0.state = L120.state. Flasher lamp mapped to f0 VPX light. Part of Flashers collection (color/brightness options). BL_F_f0 lightmap illuminates Bumper1 ring/skirt, Bumper2, KT_sw14, Parts, Plastics, Playfield, SideBlades.
- `games/stargate.json#/lamps/55._note`: L121_animate sets f1.state = L121.state. Flasher lamp mapped to f1 VPX light. BL_F_f1 lightmap illuminates DT_sw36, Glider, GuardianL/R, KT_sw15, Layer1/2, Pyramid1, RF1U, ST_sw32.
- `games/stargate.json#/lamps/56._note`: L122_animate sets f2.state = L122.state. Flasher lamp mapped to f2 VPX light. BL_F_f2 lightmap illuminates Glider, GuardianR, KT_sw15, Layer1/2, Pyramid1, ST_sw22.
- `games/stargate.json#/lamps/57._note`: L123_animate sets f3.state = L123.state. Flasher lamp mapped to f3 VPX light. BL_F_f3 lightmap illuminates Glider, GuardianR, Layer2, Pyramid1.
- `games/stargate.json#/lamps/58._note`: L124_animate sets f4.state = L124.state. Flasher lamp mapped to f4 VPX light. BL_F_f4 lightmap illuminates DT_sw26/sw36, Glider, GuardianL/R, KT_sw15, LSling, Layer1, Pyramid1, RF1, ST_sw22/sw32.
- `games/stargate.json#/lamps/59._note`: L125_animate sets f5.state = L125.state. Flasher lamp mapped to f5 VPX light. BL_F_f5 lightmap illuminates Bumper2, DT_sw17/sw26/sw27/sw35/sw36/sw37, KT_sw16, LF/RF, LSling/RSling, SarcArm, SlingL.
- `games/stargate.json#/lamps/60._note`: From BL_BC_L126 backglass lightmap array. LM_BC_L126_VRRR only. Has special color handling in SetGiColor JLou mode.
- `games/stargate.json#/_source/confidence_notes`: High confidence extraction from VPW v2.0 VBScript by mcarter78/Sixtoe/Rothbauerw/Apophis team. Platform detected as GTS3 from LoadVPM '03060000', 'GTS3.VBS', 3.10 call. ROM identified as 'stargat5' from Const cGameName. Trough is custom physical design (not cvpmTrough) using three VPX kicker objects (swTrough1, swTrough2, swTrough3) plus Drain kicker, with a manual UpdateTrough cascade timer that shifts balls between positions. Switch 34 tracks swTrough3 occupancy (ball ready) and switch 24 tracks Drain occupancy. SolRelease (sol 28) ejects from swTrough1, SolTrough (sol 29) kicks from Drain. Three VUKs: sw33 (right, kicked by sol 12 VukTopPop), sw23 (center, kicked by sol 11 BotPop), sw80 (left, kicked by sol 10 LeftPop). Glider mechanism uses two motor solenoids (sol 23 LR motor, sol 24 forward motor) driving a GliderTimer animation that sets sw21 (home position) and sw30 (right limit position) via position calculations. Pyramid mechanism (sol 16) uses LeftFlipper1 VPX object with sw102 set via delayed timer. Diverter (sol 13) uses Flipper1 VPX object and sets sw101 for position feedback. Guardian targets (sol 14 left, sol 15 right) are pivot targets that physically open/close to reveal/block sw116/sw117 standup targets. Drop targets: 3-bank left (sw17/27/37, reset sol 17), 2-bank top (sw26/36, reset sol 18), single right (sw35, reset sol 19, trip sol 20). Kicking targets sw14/15/16 use Rothbauerw KickingTarget class with animated rebound. Bumpers use PulseSw (sw10=Bumper1 bottom, sw11=Bumper2 top). Slingshots use PulseSw (sw12=left, sw13=right). Flipper solenoids from GTS3 framework constants: sLRFlipper (right), sLLFlipper (left), sURFlipper (upper right). Lamps identified from vpmMapLights AllLamps and BL_L_ lightmap arrays: L0, L5-L7, L11-L17, L21-L27, L32-L37, L41-L47, L55-L57, L65-L67, L71-L77, L81-L87, plus flasher lamps L120-L125 mapped to f0-f5 VPX light objects, and backglass lamps L90, L92, L112, L126. GI controlled by sol 31 (GIState, inverted -- Not Enabled = GI on). Backbox GI via sol 26 (SolBBGI). Rope lights via sol 22 (SolBGRopeLights). Six commented-out solenoids: 1-4 (bumpers/slingshots handled by VPX physics), 5-7 (kicking target kickbacks), 21 (not used), 25 (not used), 27 (ticket dispenser), 32 (game over relay). Wire trigger switches sw31/sw111-sw115 use Controller.Switch on/off pattern with wire animation. Ramp triggers sw90/sw100/sw110 use PulseSw. Pyramid subway switch sw91 uses PulseSw. Tournament mode switch sw5 set by RightMagnaSave key and TournamentTimer auto-set at startup. Switch sw6 (FrontDoor) set by TournamentTimer.

## Unresolved questions

- Is the I/O enumeration complete for every supported physical/controller variant?
- Which inferred VPX behaviors reflect real hardware, and which are table-script conveniences?
- Are all mechanism home states, sensors, motion constraints, and ball interactions documented?

## Sources

- `legacy.game.stargate`: `games/stargate.json` at the pinned migration revision.
