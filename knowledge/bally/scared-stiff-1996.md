# Scared Stiff

Coverage: **partial - source-derived recreation knowledge requiring validation**

## Overview

Legacy evidence identifies this candidate as Bally (1996). The information below is preserved for recreation work but is not automatically treated as validated physical-machine fact.

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
- `games/scared-stiff.json#/switches/0._note`: cvpmMech.AddSw 12, 0, 0 — Spider mechanism position switch at step 0. Used by mSpider cvpmMech to track wheel home position.
- `games/scared-stiff.json#/switches/1._note`: vpmNudge.TiltSwitch = 14.
- `games/scared-stiff.json#/switches/2._note`: Controller.Switch(16)=1 on sw16_Hit, =0 on sw16_UnHit. Also Controller.Switch(16)=0 on StartGameKey release. Dual-purpose: shooter lane rollover AND start button (common WPC pattern where start button press is handled by vpmKeyDown).
- `games/scared-stiff.json#/switches/3._note`: Controller.Switch(17) on/off. Rollover switch with rightInlaneSpeedLimit ball speed correction.
- `games/scared-stiff.json#/switches/4._note`: Controller.Switch(18) on/off. Rollover switch. plungerIM.InitImpulseP swplunger uses this area. BP_sw18 z-positioned at -23.5 on init.
- `games/scared-stiff.json#/switches/5._note`: Controller.Switch(25) on/off. Rollover switch.
- `games/scared-stiff.json#/switches/6._note`: Controller.Switch(26) on/off. Rollover switch with leftInlaneSpeedLimit ball speed correction.
- `games/scared-stiff.json#/switches/7._note`: Controller.Switch(27) on/off. Rollover switch.
- `games/scared-stiff.json#/switches/8._note`: STHit 28. Stand-up target with VPW TargetBouncer animation. vpmTimer.PulseSw(28) via STAnimate.
- `games/scared-stiff.json#/switches/9._note`: vpmTimer.PulseSw 31 fired by SolRelease (sol 9). This is the trough eject opto — pulsed when ball is kicked out of trough. Acts as drain/outhole equivalent in WPC trough design.
- `games/scared-stiff.json#/switches/10._note`: Controller.Switch(32) on/off. First trough position (nearest eject). Ball created here on init. sw32.kick called by SolRelease. UpdateTrough cascades balls forward.
- `games/scared-stiff.json#/switches/11._note`: Controller.Switch(33) on/off. Second trough position. Ball created here on init.
- `games/scared-stiff.json#/switches/12._note`: Controller.Switch(34) on/off. Third trough position. Ball created here on init.
- `games/scared-stiff.json#/switches/13._note`: Controller.Switch(35) on/off. Fourth trough position (nearest drain). Ball created here on init. 4-ball trough.
- `games/scared-stiff.json#/switches/14._note`: Controller.Switch(36)=1 on hit, cleared by scoop_right (sol 3). KickBall launches ball vertically (kvelz=30, kzlift=105). Has rampFlap animation and Subway_UpVukTrap collidable toggle. Sound debounce via sw36sfx flag.
- `games/scared-stiff.json#/switches/15._note`: Controller.Switch(37)=1 on hit, cleared by scoop_topleft (sol 6). KickBall launches ball (angle 0, vel 3, kvelz random 35-45, kzlift 50). ScoopHit sound.
- `games/scared-stiff.json#/switches/16._note`: Controller.Switch(38) on/off. Opto switch in subway/crate area.
- `games/scared-stiff.json#/switches/17._note`: Controller.Switch(41)=1 on hit, cleared by CoffinPopper (sol 4). KickBall launches ball (angle 168, vel 1, kvelz 30, kzlift 100). NOTE: Simple sw41_Hit/UnHit is commented out — replaced by VUK implementation in ZVUK section.
- `games/scared-stiff.json#/switches/18._note`: Controller.Switch(42) on/off. Centre position in coffin ball lock area.
- `games/scared-stiff.json#/switches/19._note`: Controller.Switch(43) on/off. Right position in coffin ball lock area.
- `games/scared-stiff.json#/switches/20._note`: Controller.Switch(44) on/off. Left ramp entrance switch.
- `games/scared-stiff.json#/switches/21._note`: Controller.Switch(45) on/off. Right ramp entrance switch.
- `games/scared-stiff.json#/switches/22._note`: Controller.Switch(46) on/off. Left ramp completion switch.
- `games/scared-stiff.json#/switches/23._note`: Controller.Switch(47) on/off. Right ramp completion switch.
- `games/scared-stiff.json#/switches/24._note`: Controller.Switch(48) on/off. Coffin entrance opto. sw48_Hit calls ScoopHit for sound.
- `games/scared-stiff.json#/switches/25._note`: vpmTimer.PulseSw(51). Fired from LeftSlingShot_Slingshot event. LS.VelocityCorrect applied.
- `games/scared-stiff.json#/switches/26._note`: vpmTimer.PulseSw(52). Fired from RightSlingShot_Slingshot event. RS.VelocityCorrect applied.
- `games/scared-stiff.json#/switches/27._note`: vpmTimer.PulseSw 53. Bumper1_Hit. BSocket1 skirt animation.
- `games/scared-stiff.json#/switches/28._note`: vpmTimer.PulseSw 54. Bumper2_Hit. BSocket2 skirt animation.
- `games/scared-stiff.json#/switches/29._note`: vpmTimer.PulseSw 55. Bumper3_Hit. BSocket3 skirt animation.
- `games/scared-stiff.json#/switches/30._note`: vpmTimer.PulseSw(56). Fired from TopSlingShot_Slingshot event. TS.VelocityCorrect applied. Uses LSlingArmU animation primitives.
- `games/scared-stiff.json#/switches/31._note`: Controller.Switch(57) on/off. Magnetic sensor in crate mechanism area.
- `games/scared-stiff.json#/switches/32._note`: Controller.Switch(58) on/off. Rollover switch with wire animation.
- `games/scared-stiff.json#/switches/33._note`: STHit 61. Stand-up target with VPW TargetBouncer animation. vpmTimer.PulseSw(61) via STAnimate.
- `games/scared-stiff.json#/switches/34._note`: STHit 62. Stand-up target with VPW TargetBouncer animation. vpmTimer.PulseSw(62) via STAnimate.
- `games/scared-stiff.json#/switches/35._note`: STHit 63. Stand-up target with VPW TargetBouncer animation. vpmTimer.PulseSw(63) via STAnimate.
- `games/scared-stiff.json#/switches/36._note`: STHit 64. Left frog leaper target — both a stand-up target AND animated frog (PrLeaper1). Frog bounces on hit with velocity-dependent height. vpmTimer.PulseSw(64) via STAnimate.
- `games/scared-stiff.json#/switches/37._note`: STHit 65. Center frog leaper target — both a stand-up target AND animated frog (PrLeaper2). Frog bounces on hit. vpmTimer.PulseSw(65) via STAnimate.
- `games/scared-stiff.json#/switches/38._note`: STHit 66. Right frog leaper target — both a stand-up target AND animated frog (PrLeaper3). Frog bounces on hit. vpmTimer.PulseSw(66) via STAnimate.
- `games/scared-stiff.json#/switches/39._note`: Controller.Switch(67) on/off. Rubber switch in upper right playfield area.
- `games/scared-stiff.json#/switches/40._note`: Controller.Switch(68) on/off. Rollover switch with wire animation.
- `games/scared-stiff.json#/switches/41._note`: Controller.Switch(71) on/off. Top rollover lane.
- `games/scared-stiff.json#/switches/42._note`: Controller.Switch(72) on/off. Top rollover lane.
- `games/scared-stiff.json#/switches/43._note`: Controller.Switch(73) on/off. Top rollover lane.
- `games/scared-stiff.json#/switches/44._note`: Controller.Switch(74) on/off. Rollover switch with wire animation.
- `games/scared-stiff.json#/coils/0._vbscript_callback`: AutoPlunge
- `games/scared-stiff.json#/coils/0._inferred_type`: ball_management
- `games/scared-stiff.json#/coils/0._note`: Impulse plunger auto-fire. plungerIM.AutoFire. Also enables Gate008.collidable during fire. cvpmImpulseP with power 45, time 0.6.
- `games/scared-stiff.json#/coils/1._vbscript_callback`: LoopGate
- `games/scared-stiff.json#/coils/1._inferred_type`: mechanism
- `games/scared-stiff.json#/coils/1._note`: Controls GateLoop one-way gate. GateLoop.Open = Enabled.
- `games/scared-stiff.json#/coils/2._vbscript_callback`: scoop_right
- `games/scared-stiff.json#/coils/2._inferred_type`: ball_management
- `games/scared-stiff.json#/coils/2._note`: Kicks ball out of right scoop (sw36). KickBall with angle 0, vel 0, kvelz 30, kzlift 105. Clears Controller.Switch(36). Also animates rampFlap and toggles Subway_UpVukTrap collidable.
- `games/scared-stiff.json#/coils/3._vbscript_callback`: CoffinPopper
- `games/scared-stiff.json#/coils/3._inferred_type`: ball_management
- `games/scared-stiff.json#/coils/3._note`: Kicks ball out of coffin scoop (sw41). KickBall with angle 168, vel 1, kvelz 30, kzlift 100. Clears Controller.Switch(41).
- `games/scared-stiff.json#/coils/4._vbscript_callback`: CoffinDoor
- `games/scared-stiff.json#/coils/4._inferred_type`: mechanism
- `games/scared-stiff.json#/coils/4._note`: Controls CoffinFlipper VPX flipper object. RotateToEnd on enable, RotateToStart on disable. Animated coffin door with open/closed baked map swap at angle -45.
- `games/scared-stiff.json#/coils/5._vbscript_callback`: scoop_topleft
- `games/scared-stiff.json#/coils/5._inferred_type`: ball_management
- `games/scared-stiff.json#/coils/5._note`: Kicks ball out of left scoop (sw37). KickBall with angle 0, vel 3, kvelz random 35-45, kzlift 50. Clears Controller.Switch(37).
- `games/scared-stiff.json#/coils/6._vbscript_callback`: vpmSolSound SoundFX("Knocker_1",DOFKnocker),
- `games/scared-stiff.json#/coils/6._inferred_type`: knocker
- `games/scared-stiff.json#/coils/6._note`: Cabinet knocker solenoid. Sound-only callback.
- `games/scared-stiff.json#/coils/7._vbscript_callback`: CratePostPower
- `games/scared-stiff.json#/coils/7._inferred_type`: mechanism
- `games/scared-stiff.json#/coils/7._note`: COMMENTED OUT in VBS: 'SolCallback(8) = "CratePostPower" — Not Required, just for initial power surge. See sol 16 CratePostHold for the active crate post solenoid.
- `games/scared-stiff.json#/coils/8._vbscript_callback`: SolRelease
- `games/scared-stiff.json#/coils/8._inferred_type`: ball_management
- `games/scared-stiff.json#/coils/8._note`: Ejects ball from trough. PulseSw 31 then sw32.kick 60,9. Main trough release solenoid.
- `games/scared-stiff.json#/coils/9._vbscript_callback`: SolLeftSling
- `games/scared-stiff.json#/coils/9._inferred_type`: slingshot
- `games/scared-stiff.json#/coils/9._note`: Left slingshot solenoid. Drives LeftSlingShot animation and Boogie Monster nudge (BoogLSlingNudge).
- `games/scared-stiff.json#/coils/10._vbscript_callback`: SolRightSling
- `games/scared-stiff.json#/coils/10._inferred_type`: slingshot
- `games/scared-stiff.json#/coils/10._note`: Right slingshot solenoid. Drives RightSlingShot animation and Boogie Monster nudge (BoogRSlingNudge).
- `games/scared-stiff.json#/coils/11._inferred_type`: bumper
- `games/scared-stiff.json#/coils/11._note`: COMMENTED OUT: 'SolCallBack(12) = "Centre Jet" — Not Required. Bumper coil handled by VPX physics.
- `games/scared-stiff.json#/coils/12._inferred_type`: bumper
- `games/scared-stiff.json#/coils/12._note`: COMMENTED OUT: 'SolCallBack(13) = "Upper Jet" — Not Required. Bumper coil handled by VPX physics.
- `games/scared-stiff.json#/coils/13._inferred_type`: bumper
- `games/scared-stiff.json#/coils/13._note`: COMMENTED OUT: 'SolCallBack(14) = "Lower Jet" — Not Required. Bumper coil handled by VPX physics.
- `games/scared-stiff.json#/coils/14._inferred_type`: slingshot
- `games/scared-stiff.json#/coils/14._note`: COMMENTED OUT: 'SolCallBack(15) = "Upper Sling" — Not Required. Slingshot handled by VPX physics.
- `games/scared-stiff.json#/coils/15._vbscript_callback`: CratePostHold
- `games/scared-stiff.json#/coils/15._inferred_type`: mechanism
- `games/scared-stiff.json#/coils/15._note`: Crate post hold solenoid. Crate_Pin.Collidable = Not Enabled. When energized, crate pin drops (not collidable), allowing ball passage. Sol 8 (CratePostPower) is commented out — this hold coil does all the work.
- `games/scared-stiff.json#/coils/16._vbscript_callback`: SolFlash17
- `games/scared-stiff.json#/coils/16._inferred_type`: flasher
- `games/scared-stiff.json#/coils/16._note`: SolModCallback PWM flasher. f17.state = level.
- `games/scared-stiff.json#/coils/17._vbscript_callback`: SolFlash18
- `games/scared-stiff.json#/coils/17._inferred_type`: flasher
- `games/scared-stiff.json#/coils/17._note`: SolModCallback PWM flasher. f18.state = level.
- `games/scared-stiff.json#/coils/18._vbscript_callback`: SolFlash19
- `games/scared-stiff.json#/coils/18._inferred_type`: flasher
- `games/scared-stiff.json#/coils/18._note`: SolModCallback PWM flasher. f19.state = level.
- `games/scared-stiff.json#/coils/19._vbscript_callback`: SolFlash20
- `games/scared-stiff.json#/coils/19._inferred_type`: flasher
- `games/scared-stiff.json#/coils/19._note`: SolModCallback PWM flasher. Drives f20.state AND f20a.state (two flasher objects).
- `games/scared-stiff.json#/coils/20._vbscript_callback`: SolFlash21
- `games/scared-stiff.json#/coils/20._inferred_type`: flasher
- `games/scared-stiff.json#/coils/20._note`: SolModCallback PWM flasher. f21.state = level.
- `games/scared-stiff.json#/coils/21._vbscript_callback`: SolFlash22
- `games/scared-stiff.json#/coils/21._inferred_type`: flasher
- `games/scared-stiff.json#/coils/21._note`: SolModCallback PWM flasher. f22.state = level.
- `games/scared-stiff.json#/coils/22._vbscript_callback`: SolFlash23
- `games/scared-stiff.json#/coils/22._inferred_type`: flasher
- `games/scared-stiff.json#/coils/22._note`: SolModCallback PWM flasher. Drives f23.state AND f23a.state (two flasher objects — inside boney skull).
- `games/scared-stiff.json#/coils/23._vbscript_callback`: SolFlash24
- `games/scared-stiff.json#/coils/23._inferred_type`: flasher
- `games/scared-stiff.json#/coils/23._note`: SolModCallback PWM flasher. f24.state = level.
- `games/scared-stiff.json#/coils/24._vbscript_callback`: SolFlash25
- `games/scared-stiff.json#/coils/24._inferred_type`: flasher
- `games/scared-stiff.json#/coils/24._note`: SolModCallback PWM flasher. f25.state = level.
- `games/scared-stiff.json#/coils/25._vbscript_callback`: SolFlash26
- `games/scared-stiff.json#/coils/25._inferred_type`: flasher
- `games/scared-stiff.json#/coils/25._note`: SolModCallback PWM flasher. f26.state = level.
- `games/scared-stiff.json#/coils/26._vbscript_callback`: SolFlash27
- `games/scared-stiff.json#/coils/26._inferred_type`: flasher
- `games/scared-stiff.json#/coils/26._note`: SolModCallback PWM flasher. f27.state = level.
- `games/scared-stiff.json#/coils/27._vbscript_callback`: SolFlash28
- `games/scared-stiff.json#/coils/27._inferred_type`: flasher
- `games/scared-stiff.json#/coils/27._note`: SolModCallback PWM flasher. f28.state = level.
- `games/scared-stiff.json#/coils/28._vbscript_callback`: DiverterPower
- `games/scared-stiff.json#/coils/28._inferred_type`: diverter
- `games/scared-stiff.json#/coils/28._note`: Lock diverter power solenoid. LockFlipper.RotateToEnd on enable. Controls DiverterWall/DiverterWall001 drop states. Dual-solenoid design with sol 34 (DiverterHold). Both must be off for diverter to retract.
- `games/scared-stiff.json#/coils/29._vbscript_callback`: DiverterHold
- `games/scared-stiff.json#/coils/29._inferred_type`: diverter
- `games/scared-stiff.json#/coils/29._note`: Lock diverter hold solenoid. Keeps diverter in position without full power. When disabled AND DiverterPower is off, LockFlipper.RotateToStart and walls reset. Dual-solenoid power/hold design.
- `games/scared-stiff.json#/coils/30._vbscript_callback`: SolFlash35
- `games/scared-stiff.json#/coils/30._inferred_type`: flasher
- `games/scared-stiff.json#/coils/30._note`: SolModCallback PWM flasher. f35.state = level.
- `games/scared-stiff.json#/coils/31._vbscript_callback`: SolFlash36
- `games/scared-stiff.json#/coils/31._inferred_type`: flasher
- `games/scared-stiff.json#/coils/31._note`: SolModCallback PWM flasher. f36.state = level.
- `games/scared-stiff.json#/coils/32._vbscript_callback`: cvpmMech (mSpider.Sol1 = 39)
- `games/scared-stiff.json#/coils/32._inferred_type`: mechanism
- `games/scared-stiff.json#/coils/32._note`: Spider wheel mechanism first solenoid. cvpmMech with vpmMechStepSol + vpmMechCircle + vpmMechLinear + vpmMechFast. 48 steps, length 200. Drives pSpider/pSpider2 rotation via UpdateSpider callback. Not in SolCallback — consumed by framework.
- `games/scared-stiff.json#/coils/33._vbscript_callback`: cvpmMech (mSpider.Sol2 = 40)
- `games/scared-stiff.json#/coils/33._inferred_type`: mechanism
- `games/scared-stiff.json#/coils/33._note`: Spider wheel mechanism second solenoid. Part of dual-solenoid step motor (vpmMechStepSol). Works with sol 39 to control spider wheel position and direction.
- `games/scared-stiff.json#/lamps/37._note`: Also has secondary VPX light l56a (separate lightmap group LM_L_l56a, secondary illumination zone for same lamp circuit).
- `games/scared-stiff.json#/_source/confidence_notes`: High confidence extraction from VPW v1.1.1 VBScript. Platform detected as WPC from LoadVPM call ('WPC.VBS'). ROM name 'SS_15' from Const cGameName. Trough is a 4-ball manual implementation (not cvpmTrough) using kicker objects sw32-sw35 with Controller.Switch on/off and an UpdateTrough timer that cascades balls forward (sw32.BallCntOver check). Ball release via SolRelease (sol 9) which PulseSw 31 and kicks from sw32. Drain_Hit kicks ball back into trough with 500ms delay. No Lampz.MassAssign — uses UseLamps=1 with vpmMapLights AllLamps (VPX light timer interval maps lamp IDs). Lamp IDs extracted from VLM baked lightmap arrays (LM_L_l## references in commented BL_L_l## definitions). Flashers use SolModCallback with UseVPMModSol=2 for PWM control. Spider wheel mechanism uses cvpmMech (vpmMechStepSol + vpmMechCircle + vpmMechLinear + vpmMechFast, sol1=39, sol2=40, AddSw 12 at position 0, 48 steps, length 200). Coffin diverter is a dual-solenoid power/hold design (sol 33 DiverterPower, sol 34 DiverterHold) controlling LockFlipper VPX object and DiverterWall drop states. Coffin door (sol 5) controls CoffinFlipper. VUKs for sw36 (right scoop), sw37 (left scoop), sw41 (coffin popper) use manual KickBall with Controller.Switch tracking — no cvpmBallStack. Crate post hold (sol 16) controls Crate_Pin collidable state. Stand-up targets (sw28, sw61-66) use STHit which calls vpmTimer.PulseSw(switch mod 100). Slingshots use PulseSw (51 left, 52 right, 56 upper). Bumpers use PulseSw (53 upper, 54 centre, 55 lower). Flipper solenoids use WPC framework constants sLRFlipper/sLLFlipper. NoUpperRightFlipper and NoUpperLeftFlipper called. SolCallback(8) for CratePostPower is commented out. SolCallbacks 12-15 commented out (Centre Jet, Upper Jet, Lower Jet, Upper Sling — handled by VPX physics). Coffin trough sw41 has both a commented-out simple switch version AND a VUK implementation (sw41_Hit in ZVUK section). GI handled via UseVPMModSol=2 with VLM lightmap system (GIC and GIU arrays for GI strings).

## Unresolved questions

- Is the I/O enumeration complete for every supported physical/controller variant?
- Which inferred VPX behaviors reflect real hardware, and which are table-script conveniences?
- Are all mechanism home states, sensors, motion constraints, and ball interactions documented?

## Sources

- `legacy.game.scared-stiff`: `games/scared-stiff.json` at the pinned migration revision.
