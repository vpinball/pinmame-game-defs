# Harlem Globetrotters on Tour

Coverage: **partial - source-derived recreation knowledge requiring validation**

## Overview

Legacy evidence identifies this candidate as Bally (1979). The information below is preserved for recreation work but is not automatically treated as validated physical-machine fact.

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

- `platforms/bally.json#/coils/1`: Unbound legacy outputs record `c_flipper_lower_right` was retained as a migration note only.
- `platforms/bally.json#/coils/2`: Unbound legacy outputs record `c_flipper_lower_left` was retained as a migration note only.
- `platforms/bally.json#/coils/3`: Unbound legacy outputs record `c_flipper_upper_right` was retained as a migration note only.
- `platforms/bally.json#/coils/4`: Unbound legacy outputs record `c_flipper_upper_left` was retained as a migration note only.
- `games/harlem-globetrotters.json#/switches/0._note`: DTHit 1 on sw1_hit. Drop target framework class instance DT1. Controller.Switch(1) set to 1 when dropped, 0 when raised. Reset by sol 15.
- `games/harlem-globetrotters.json#/switches/1._note`: DTHit 2 on sw2_hit. Drop target framework class instance DT2. Controller.Switch(2) set to 1 when dropped, 0 when raised. Reset by sol 15.
- `games/harlem-globetrotters.json#/switches/2._note`: DTHit 3 on sw3_hit. Drop target framework class instance DT3. Controller.Switch(3) set to 1 when dropped, 0 when raised. Reset by sol 15.
- `games/harlem-globetrotters.json#/switches/3._note`: DTHit 4 on sw4_hit. Drop target framework class instance DT4. Controller.Switch(4) set to 1 when dropped, 0 when raised. Reset by sol 15.
- `games/harlem-globetrotters.json#/switches/4._note`: Controller.Switch(8) on/off in Drain_Hit/Drain_UnHit. Single-ball Bally -35 outhole. Ball created in Drain at init with Switch(8)=1. SolBallRelease (sol 7) kicks ball out.
- `games/harlem-globetrotters.json#/switches/5._note`: vpmTimer.PulseSw 17 in sw17_Spin. Spinner with VLM frame animation (sw17_FrameAnimate).
- `games/harlem-globetrotters.json#/switches/6._note`: Controller.Switch(22) on/off in sw22_Hit/sw22_UnHit. Has VLM baked part BP_Rollover_sw22.
- `games/harlem-globetrotters.json#/switches/7._note`: Controller.Switch(23) on/off in sw23_Hit/sw23_UnHit. Has VLM baked part BP_Rollover_sw23 and sw23_Animate sub.
- `games/harlem-globetrotters.json#/switches/8._note`: Controller.Switch(24)=1 on sw24_Hit. Cleared by SolTopSaucer (sol 13) which kicks ball with sw24.kick. SoundSaucerLock on entry.
- `games/harlem-globetrotters.json#/switches/9._note`: vpmTimer.PulseSw 25 in sw25_Spin. Spinner with VLM frame animation (sw25_FrameAnimate).
- `games/harlem-globetrotters.json#/switches/10._note`: vpmTimer.PulseSw 26 in sw26_Hit with STHit animation. Has bounce overlay sw26o_Hit with TargetBouncer. VLM baked part BP_STsw26.
- `games/harlem-globetrotters.json#/switches/11._note`: vpmTimer.PulseSw 27 in sw27_Hit with STHit animation. Has bounce overlay sw27o_Hit with TargetBouncer. VLM baked part BP_STsw27.
- `games/harlem-globetrotters.json#/switches/12._note`: vpmTimer.PulseSw 28 in sw28_Hit with STHit animation. Has bounce overlay sw28o_Hit with TargetBouncer. VLM baked part BP_STsw28.
- `games/harlem-globetrotters.json#/switches/13._note`: vpmTimer.PulseSw 29 in sw29_Hit with STHit animation. Has bounce overlay sw29o_Hit with TargetBouncer. VLM baked part BP_STsw29.
- `games/harlem-globetrotters.json#/switches/14._note`: vpmTimer.PulseSw 30 in sw30_Hit with STHit animation. Has bounce overlay sw30o_Hit with TargetBouncer. VLM baked part BP_STsw30.
- `games/harlem-globetrotters.json#/switches/15._note`: Controller.Switch(31) on/off in sw31_Hit/sw31_UnHit. Has VLM baked part BP_Rollover_sw31.
- `games/harlem-globetrotters.json#/switches/16._note`: Controller.Switch(32)=1 on sw32_Hit. Cleared by SolRightSaucer (sol 14) which kicks ball with sw32.kick. SoundSaucerLock on entry.
- `games/harlem-globetrotters.json#/switches/17._note`: vpmTimer.PulseSw 33 in sw33_Spin. Spinner with VLM frame animation (sw33_FrameAnimate).
- `games/harlem-globetrotters.json#/switches/18._note`: vpmTimer.PulseSw 34 in sw34_Hit. Also triggered by RubberBand20_Hit and RubberBand21_Hit (PulseSw 34). Leaf switch per VPW changelog.
- `games/harlem-globetrotters.json#/switches/19._note`: vpmTimer.PulseSw 35 in sw35_Hit with STHit animation. Has bounce overlay sw35o_Hit with TargetBouncer. VLM baked part BP_STsw35.
- `games/harlem-globetrotters.json#/switches/20._note`: vpmTimer.PulseSw 36 in RightSlingShot_Slingshot event. Fired from slingshot event handler with sound and animation.
- `games/harlem-globetrotters.json#/switches/21._note`: vpmTimer.PulseSw 37 in LeftSlingShot_Slingshot event. Fired from slingshot event handler with sound and animation.
- `games/harlem-globetrotters.json#/switches/22._note`: vpmTimer.PulseSw 38 in Bumper2_Hit. RandomSoundBumperMiddle. VLM baked parts BP_Bumper2_Socket, BP_Bumper2_ring.
- `games/harlem-globetrotters.json#/switches/23._note`: vpmTimer.PulseSw 39 in Bumper3_Hit. RandomSoundBumperBottom. VLM baked parts BP_Bumper3_Socket, BP_Bumper3_ring.
- `games/harlem-globetrotters.json#/switches/24._note`: vpmTimer.PulseSw 40 in Bumper1_Hit. RandomSoundBumperTop. VLM baked parts BP_Bumper1_Socket, BP_Bumper1_ring.
- `games/harlem-globetrotters.json#/switches/25._note`: vpmTimer.PulseSw 134 in sw34a_Hit. Separate leaf switch mapped to PinMAME switch 134. Bally -35 extended switch addressing. Added in VPW 1.15 per changelog.
- `games/harlem-globetrotters.json#/coils/0._vbscript_callback`: vpmSolSound SoundFX("fx_Knocker",DOFKnocker),
- `games/harlem-globetrotters.json#/coils/0._inferred_type`: knocker
- `games/harlem-globetrotters.json#/coils/0._note`: Cabinet knocker solenoid. Sound-only callback via vpmSolSound.
- `games/harlem-globetrotters.json#/coils/1._vbscript_callback`: SolBallRelease
- `games/harlem-globetrotters.json#/coils/1._inferred_type`: ball_management
- `games/harlem-globetrotters.json#/coils/1._note`: Kicks ball from Drain kicker at angle 57, power 20. Single-ball Bally -35 outhole mechanism -- no trough, just outhole and kicker.
- `games/harlem-globetrotters.json#/coils/2._vbscript_callback`: SolTopSaucer
- `games/harlem-globetrotters.json#/coils/2._inferred_type`: ball_management
- `games/harlem-globetrotters.json#/coils/2._note`: Kicks ball from top saucer (sw24) with sw24.kick at angle ~200 (with random variance), power 10. Clears Controller.Switch(24).
- `games/harlem-globetrotters.json#/coils/3._vbscript_callback`: SolRightSaucer
- `games/harlem-globetrotters.json#/coils/3._inferred_type`: ball_management
- `games/harlem-globetrotters.json#/coils/3._note`: Kicks ball from right saucer (sw32) with sw32.kick at angle -45, power 20. Clears Controller.Switch(32).
- `games/harlem-globetrotters.json#/coils/4._vbscript_callback`: dtDropreset
- `games/harlem-globetrotters.json#/coils/4._inferred_type`: drop_target_reset
- `games/harlem-globetrotters.json#/coils/4._note`: Resets all 4 drop targets (DTRaise 1-4). Calls RandomSoundDropTargetReset. Sets Controller.Switch(1-4) to 0 via DTAnimate framework.
- `games/harlem-globetrotters.json#/coils/5._vbscript_callback`: Soldiv
- `games/harlem-globetrotters.json#/coils/5._inferred_type`: diverter
- `games/harlem-globetrotters.json#/coils/5._note`: Controls RightLaneGate via vpmSolDiverter. Inverted logic (Not Enabled). VLM primitive BP_Diverter animated to track gate angle.
- `games/harlem-globetrotters.json#/coils/6._vbscript_callback`: vpmNudge.SolGameOn
- `games/harlem-globetrotters.json#/coils/6._inferred_type`: mechanism
- `games/harlem-globetrotters.json#/coils/6._note`: Standard Bally -35 game-on relay. Passed to vpmNudge.SolGameOn framework handler.
- `games/harlem-globetrotters.json#/coils/7._vbscript_callback`: SolRFlipper
- `games/harlem-globetrotters.json#/coils/7._inferred_type`: flipper
- `games/harlem-globetrotters.json#/coils/7._note`: sLRFlipper framework constant from bally.vbs (value 33 for Bally -35). nFozzy flipper implementation. RF.Fire on enable.
- `games/harlem-globetrotters.json#/coils/8._vbscript_callback`: SolLFlipper
- `games/harlem-globetrotters.json#/coils/8._inferred_type`: flipper
- `games/harlem-globetrotters.json#/coils/8._note`: sLLFlipper framework constant from bally.vbs (value 35 for Bally -35). nFozzy flipper implementation. LF.Fire on enable.
- `games/harlem-globetrotters.json#/coils/9._vbscript_callback`: SolLFlipper1
- `games/harlem-globetrotters.json#/coils/9._inferred_type`: flipper
- `games/harlem-globetrotters.json#/coils/9._note`: sULFlipper framework constant from bally.vbs (value 37 for Bally -35). nFozzy flipper implementation. LF1.Fire on enable. Also activated by left flipper button (KeyDown chains both).
- `games/harlem-globetrotters.json#/lamps/0._note`: VLM lightmap BL_L_l1. Illuminates flipper primitives (LFlipperU, RFlipperU) and Playfield.
- `games/harlem-globetrotters.json#/lamps/4._note`: VLM illuminates Parts, Playfield, and Spinner_sw33 primitives.
- `games/harlem-globetrotters.json#/lamps/12._note`: Backglass lamp. Proxied via l13a_animate: l13.SetValue l13a.state.
- `games/harlem-globetrotters.json#/lamps/15._note`: VLM illuminates LFlipperU and Playfield.
- `games/harlem-globetrotters.json#/lamps/24._note`: Wide-area lamp. VLM illuminates bumpers, drop targets, slingshots, ramps, standup targets, spinners, and playfield.
- `games/harlem-globetrotters.json#/lamps/25._note`: Backglass lamp. Proxied via l27a_animate: l27.SetValue l27a.state.
- `games/harlem-globetrotters.json#/lamps/27._note`: Backglass lamp. Proxied via l29a_animate: l29.SetValue l29a.state.
- `games/harlem-globetrotters.json#/lamps/30._note`: VLM illuminates Playfield and RFlipperU.
- `games/harlem-globetrotters.json#/lamps/32._note`: VLM illuminates Parts, Playfield, and Spinner_sw25 primitives.
- `games/harlem-globetrotters.json#/lamps/35._note`: VLM illuminates Parts, Playfield, and Spinner_sw17 primitives.
- `games/harlem-globetrotters.json#/lamps/37._note`: VLM illuminates LeftSling1, Parts, Playfield, and Ramp2.
- `games/harlem-globetrotters.json#/lamps/39._note`: Wide-area lamp. VLM illuminates bumpers, gates, ramps, spinners, standup targets, and playfield.
- `games/harlem-globetrotters.json#/lamps/42._note`: Backglass lamp. Proxied via l45a_animate: l45.SetValue l45a.state.
- `games/harlem-globetrotters.json#/lamps/47._note`: VLM illuminates Parts, Playfield, and Spinner_sw33 primitives.
- `games/harlem-globetrotters.json#/lamps/50._note`: VLM illuminates Parts, Playfield, Spinner_sw17 primitives including wire.
- `games/harlem-globetrotters.json#/lamps/54._note`: VLM Parts only -- no Playfield lightmap.
- `games/harlem-globetrotters.json#/lamps/55._note`: VLM illuminates Parts, apron1, and hg_apron2_003.
- `games/harlem-globetrotters.json#/lamps/57._note`: Backglass lamp. Proxied via l61a_animate: l61.SetValue l61a.state.
- `games/harlem-globetrotters.json#/_source/confidence_notes`: High confidence extraction from VPW 1.0 release by mcarter78/apophis/team. Platform is Bally -35 era, loaded via LoadVPM '03060000', 'bally.vbs', 3.02. No cvpmTrough framework -- this is a pre-trough-era single-ball game. Ball management uses a single Drain kicker: ball is created in Drain at init with Controller.Switch(8)=1, Drain_Hit sets switch 8 on, SolBallRelease (sol 7) kicks ball out via Drain.kick. No trough switches at all -- Bally -35 games used a simple outhole/ball release mechanism. Switches identified from _Hit/_UnHit subs, PulseSw calls, and Controller.Switch() calls. Drop targets sw1-4 use the DTHit/DTRaise framework class with DTAnimate setting controller.Switch(switchid mod 100). Sw34a fires PulseSw 134 (second leaf switch mapped to different ROM column, common Bally -35 pattern). Two saucers: sw24 (top, sol 13 kicks) and sw32 (right, sol 14 kicks) use Controller.Switch on/off. Three spinners: sw17, sw25, sw33 (PulseSw). Six standup targets: sw26-30, sw35 (PulseSw with STHit animation). Three bumpers: sw40 (Bumper1/top), sw38 (Bumper2/middle), sw39 (Bumper3/bottom). Two slingshots: sw37 (left), sw36 (right) via PulseSw. Three rollovers: sw22, sw23, sw31 (Controller.Switch on/off). Leaf switches: sw34 (PulseSw 34), sw34a (PulseSw 134). Diverter on sol 17 controls RightLaneGate via vpmSolDiverter with inverted logic. GI is manually managed (UseGI=0) -- ToggleGI sub turns on/off all GI lights based on ball count (GIUpdate checks GetBalls); GiOn/GiOff defined in bally.vbs framework. Flipper solenoid IDs come from bally.vbs framework constants (sLRFlipper, sLLFlipper, sULFlipper) -- for Bally -35, these are typically sol 33 (right), sol 35 (left), sol 37 (upper left). Game has two lower flippers and one upper left flipper. ROM name uses bootleg 7-digit ROM 'hglbtrtb' (normal 6-digit 'hglbtrtr' is commented out). Lamps identified from VLM lightmap arrays (BL_L_l* naming convention). VLM system uses baked lightmaps per lamp for real-time rendering. Backglass lamps (l13, l27, l29, l45, l61) identified via _animate subs that proxy from backglass light objects. Several VLM lamps have secondary objects (l42b, l200, l360, l500, l520) for additional light positions.

## Unresolved questions

- Is the I/O enumeration complete for every supported physical/controller variant?
- Which inferred VPX behaviors reflect real hardware, and which are table-script conveniences?
- Are all mechanism home states, sensors, motion constraints, and ball interactions documented?

## Sources

- `legacy.game.harlem-globetrotters`: `games/harlem-globetrotters.json` at the pinned migration revision.
