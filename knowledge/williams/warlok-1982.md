# Warlok

Coverage: **partial - source-derived recreation knowledge requiring validation**

## Overview

Legacy evidence identifies this candidate as Williams (1982). The information below is preserved for recreation work but is not automatically treated as validated physical-machine fact.

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

- `games/warlok.json#/switches/0._note`: vpmNudge.TiltSwitch = 1. Sensitivity = 3. TiltObj = Array(Bumper1, LeftSlingshot, RightSlingshot).
- `games/warlok.json#/switches/1._note`: Controller.Switch(9) set on Drain_Hit/Drain_UnHit. Ball pre-created at init (Drain.Createball, Controller.Switch(9)=1). Single-ball drain, no trough — typical System 7 design.
- `games/warlok.json#/switches/2._note`: sw10_Spin sub fires vpmTimer.PulseSw(10). Spinner object with VLM rod animation (BM_Spin1Rod).
- `games/warlok.json#/switches/3._note`: sw11_Spin sub fires vpmTimer.PulseSw(11). Spinner object with VLM rod animation (BM_Spin2Rod).
- `games/warlok.json#/switches/4._note`: sw12_Spin sub fires vpmTimer.PulseSw(12). Spinner object with VLM rod animation (BM_Spin3Rod).
- `games/warlok.json#/switches/5._note`: Bumper1_Hit fires vpmTimer.PulseSw 13. Has VLM skirt animation (BP_Bumper1Skirt).
- `games/warlok.json#/switches/6._note`: Bumper2_Hit fires vpmTimer.PulseSw 14. Has VLM skirt animation (BP_Bumper2Skirt). Sound: RandomSoundBumperMiddle.
- `games/warlok.json#/switches/7._note`: Bumper3_Hit fires vpmTimer.PulseSw 15. Has VLM skirt animation (BP_Bumper3Skirt). Sound: RandomSoundBumperTop.
- `games/warlok.json#/switches/8._note`: Controller.Switch(16) on/off via sw16_Hit/sw16_UnHit. Grouped with other wire triggers. VLM wire animation (CurrentAnimOffset).
- `games/warlok.json#/switches/9._note`: Controller.Switch(17) on/off via sw17_Hit/sw17_UnHit. Grouped with other wire triggers.
- `games/warlok.json#/switches/10._note`: Controller.Switch(18) on/off via sw18_Hit/sw18_UnHit. Grouped with other wire triggers.
- `games/warlok.json#/switches/11._note`: Tsw19_Hit fires PrimStandupTgtHit 19 (animated standup target with BM_HT primitive) then vpmTimer.PulseSw 19.
- `games/warlok.json#/switches/12._note`: LeftSlingShot_Slingshot fires vpmTimer.PulseSw 20. Has 3-frame VLM sling arm animation (BP_LSling1, BP_LSling2, BP_LSlingArm).
- `games/warlok.json#/switches/13._note`: RightSlingShot_Slingshot fires vpmTimer.PulseSw 21. Has 3-frame VLM sling arm animation (BP_RSling1, BP_RSling2, BP_RSlingArm).
- `games/warlok.json#/switches/14._note`: Controller.Switch(22) on/off via sw22_Hit/sw22_UnHit. Grouped under 'rollunder gates' comment.
- `games/warlok.json#/switches/15._note`: Controller.Switch(23) on/off via sw23_Hit/sw23_UnHit. Grouped under 'Wire Triggers' comment. VLM animation.
- `games/warlok.json#/switches/16._note`: Controller.Switch(24) on/off via sw24_Hit/sw24_UnHit. Grouped under 'Wire Triggers' comment. VLM animation.
- `games/warlok.json#/switches/17._note`: Controller.Switch(25) on/off via sw25_Hit/sw25_UnHit. Grouped under 'Wire Triggers' comment. VLM animation.
- `games/warlok.json#/switches/18._note`: Controller.Switch(26) on/off via sw26_Hit/sw26_UnHit. Grouped under 'Wire Triggers' comment. VLM animation.
- `games/warlok.json#/switches/19._note`: Sw27_Hit calls DTHit 27. Part of Bank 1 (sw27-29). DT27 = new DropTarget(sw27, sw27y, BM_DT1_1, 27). Reset by Sol 1 (Sol1DropUp).
- `games/warlok.json#/switches/20._note`: Sw28_Hit calls DTHit 28. Part of Bank 1 (sw27-29). DT28 = new DropTarget(sw28, sw28y, BM_DT1_2, 28). Reset by Sol 1.
- `games/warlok.json#/switches/21._note`: Sw29_Hit calls DTHit 29. Part of Bank 1 (sw27-29). DT29 = new DropTarget(sw29, sw29y, BM_DT1_3, 29). Reset by Sol 1.
- `games/warlok.json#/switches/22._note`: Sw30_Hit calls DTHit 30. Part of Bank 2 (sw30-32). DT30 = new DropTarget(sw30, sw30y, BM_DT2_1, 30). Reset by Sol 2 (Sol2DropUp).
- `games/warlok.json#/switches/23._note`: Sw31_Hit calls DTHit 31. Part of Bank 2 (sw30-32). DT31 = new DropTarget(sw31, sw31y, BM_DT2_2, 31). Reset by Sol 2.
- `games/warlok.json#/switches/24._note`: Sw32_Hit calls DTHit 32. Part of Bank 2 (sw30-32). DT32 = new DropTarget(sw32, sw32y, BM_DT2_3, 32). Reset by Sol 2.
- `games/warlok.json#/switches/25._note`: Sw33_Hit calls DTHit 33. Part of Bank 3 (sw33-35). DT33 = new DropTarget(sw33, sw33y, BM_DT3_1, 33). Reset by Sol 3 (Sol3DropUp). Also individually dropped by Sol 5 (dt1drop).
- `games/warlok.json#/switches/26._note`: Sw34_Hit calls DTHit 34. Part of Bank 3 (sw33-35). DT34 = new DropTarget(sw34, sw34y, BM_DT3_2, 34). Reset by Sol 3. Also individually dropped by Sol 6 (dt2drop).
- `games/warlok.json#/switches/27._note`: Sw35_Hit calls DTHit 35. Part of Bank 3 (sw33-35). DT35 = new DropTarget(sw35, sw35y, BM_DT3_3, 35). Reset by Sol 3. Also individually dropped by Sol 7 (dt3drop).
- `games/warlok.json#/switches/28._note`: Controller.Switch(36)=1 on RightFlipperKey down, =0 on key up. Used for lane change or special feature — not a playfield switch. Set directly from keyboard handler.
- `games/warlok.json#/switches/29._note`: Controller.Switch(37) on/off via sw37_Hit/sw37_UnHit. Grouped under 'rollunder gates' comment.
- `games/warlok.json#/switches/30._note`: Controller.Switch(38) on/off via sw38_Hit/sw38_UnHit. Grouped under 'rollunder gates' comment.
- `games/warlok.json#/coils/0._vbscript_callback`: Sol1DropUp
- `games/warlok.json#/coils/0._inferred_type`: drop_target_reset
- `games/warlok.json#/coils/0._note`: Raises drop targets sw27, sw28, sw29 (Bank 1) via DTRaise. Sound: RandomSoundDropTargetReset.
- `games/warlok.json#/coils/1._vbscript_callback`: Sol2DropUp
- `games/warlok.json#/coils/1._inferred_type`: drop_target_reset
- `games/warlok.json#/coils/1._note`: Raises drop targets sw30, sw31, sw32 (Bank 2) via DTRaise. Sound: RandomSoundDropTargetReset.
- `games/warlok.json#/coils/2._vbscript_callback`: Sol3DropUp
- `games/warlok.json#/coils/2._inferred_type`: drop_target_reset
- `games/warlok.json#/coils/2._note`: Raises drop targets sw33, sw34, sw35 (Bank 3) via DTRaise. Sound: RandomSoundDropTargetReset.
- `games/warlok.json#/coils/3._vbscript_callback`: SolRelease
- `games/warlok.json#/coils/3._inferred_type`: ball_management
- `games/warlok.json#/coils/3._note`: Kicks ball from Drain kicker (Drain.kick 66,20). Checks BallCntOver for sound selection. No trough — simple single-ball drain/release mechanism typical of System 7.
- `games/warlok.json#/coils/4._vbscript_callback`: dt1drop
- `games/warlok.json#/coils/4._inferred_type`: drop_target
- `games/warlok.json#/coils/4._note`: Raises individual drop target sw33 (Bank 3, Target 1) via DTRaise 33. Sound: RandomSoundDropTargetReset.
- `games/warlok.json#/coils/5._vbscript_callback`: dt2drop
- `games/warlok.json#/coils/5._inferred_type`: drop_target
- `games/warlok.json#/coils/5._note`: Raises individual drop target sw34 (Bank 3, Target 2) via DTRaise 34. Sound: RandomSoundDropTargetReset.
- `games/warlok.json#/coils/6._vbscript_callback`: dt3drop
- `games/warlok.json#/coils/6._inferred_type`: drop_target
- `games/warlok.json#/coils/6._note`: Raises individual drop target sw35 (Bank 3, Target 3) via DTRaise 35. Sound: RandomSoundDropTargetReset.
- `games/warlok.json#/coils/7._vbscript_callback`: SolGi
- `games/warlok.json#/coils/7._inferred_type`: gi_relay
- `games/warlok.json#/coils/7._note`: GI relay with INVERTED logic — when enabled, GI turns OFF (all lights in GI collection set to state=0). When disabled, GI turns ON. Comment says 'The GI is inverted for some reason when the Orbit shot is made (MetaTed hack fix)'. Initialized with SolGi(False) at table init to turn GI on.
- `games/warlok.json#/coils/8._vbscript_callback`: SolRFlipper
- `games/warlok.json#/coils/8._inferred_type`: flipper
- `games/warlok.json#/coils/8._note`: sLRFlipper=14 (S7.VBS framework constant). nFozzy flipper implementation with RF.Fire, ReflipAngle=20, live catch, FlipperTricks. EOSTnew=1.5 (EM to late 80s setting).
- `games/warlok.json#/coils/9._vbscript_callback`: SolKnocker
- `games/warlok.json#/coils/9._inferred_type`: knocker
- `games/warlok.json#/coils/9._note`: Cabinet knocker solenoid. Calls KnockerSolenoid sound function.
- `games/warlok.json#/coils/10._vbscript_callback`: SolLFlipper
- `games/warlok.json#/coils/10._inferred_type`: flipper
- `games/warlok.json#/coils/10._note`: sLLFlipper=16 (S7.VBS framework constant). nFozzy flipper implementation with LF.Fire, ReflipAngle=20, live catch, FlipperTricks. EOSTnew=1.5 (EM to late 80s setting).
- `games/warlok.json#/coils/11._vbscript_callback`: vpmNudge.SolGameOn
- `games/warlok.json#/coils/11._inferred_type`: mechanism
- `games/warlok.json#/coils/11._note`: Game-on solenoid handled by VPM framework. Controls nudge/tilt enable state.
- `games/warlok.json#/lamps/0._note`: Backglass indicator lamp. Controller.Lamp(2) drives gi27 VPX object via LampCallback/UpdateMultipleLamps.
- `games/warlok.json#/lamps/1._note`: Backglass indicator lamp. Controller.Lamp(3) drives gi29 VPX object via UpdateMultipleLamps.
- `games/warlok.json#/lamps/2._note`: Backglass indicator lamp. Controller.Lamp(4) drives gi25 VPX object via UpdateMultipleLamps.
- `games/warlok.json#/lamps/3._note`: Backglass indicator lamp. Controller.Lamp(5) drives gi28 VPX object via UpdateMultipleLamps.
- `games/warlok.json#/lamps/4._note`: Backglass indicator lamp. Controller.Lamp(6) drives gi30 VPX object via UpdateMultipleLamps.
- `games/warlok.json#/lamps/5._note`: Playfield insert lamp. VLM lightmap array BL_L_L8 with Inserts, Parts, Playfield primitives.
- `games/warlok.json#/lamps/6._note`: Playfield insert lamp. VLM lightmap array BL_L_L9 with Inserts, Parts, Playfield, Spin1 primitives.
- `games/warlok.json#/lamps/7._note`: Playfield insert lamp. VLM lightmap array BL_L_L10 with Gate_4, Inserts, Parts, Playfield, Spin2 primitives.
- `games/warlok.json#/lamps/8._note`: Playfield insert lamp. VLM lightmap array BL_L_L11 with Inserts, Parts, Playfield, Spin3 primitives.
- `games/warlok.json#/lamps/9._note`: Playfield insert lamp. VLM lightmap array BL_L_L12 with Gate_1, Inserts, Parts, Playfield primitives.
- `games/warlok.json#/lamps/10._note`: Playfield insert lamp. VLM lightmap array BL_L_L13 with Inserts, Parts, Playfield primitives.
- `games/warlok.json#/lamps/11._note`: Playfield insert lamp. VLM lightmap array BL_L_L14 with Gate_6, Inserts, Parts, Playfield primitives.
- `games/warlok.json#/lamps/12._note`: Backglass indicator lamp AND playfield insert. Controller.Lamp(15) drives gi26 via UpdateMultipleLamps. Also has VLM lightmap array BL_L_L15 with FlipperR, FlipperRup, Inserts, Parts, Playfield, RSling primitives.
- `games/warlok.json#/lamps/13._note`: Playfield insert lamp. VLM lightmap array BL_L_L16 with Inserts, Parts, Playfield primitives.
- `games/warlok.json#/lamps/14._note`: Playfield insert lamp. VLM lightmap array BL_L_L17 with Inserts, Parts, Playfield primitives.
- `games/warlok.json#/lamps/15._note`: Playfield insert lamp. VLM lightmap array BL_L_L18 with Gate_5, Inserts, Parts, Playfield primitives.
- `games/warlok.json#/lamps/16._note`: Playfield insert lamp near Bumper 1. VLM lightmap array BL_L_L19 with BR1, Bumper1Skirt, HT, Inserts, Parts, Playfield primitives.
- `games/warlok.json#/lamps/17._note`: Playfield insert lamp near Drop Target Bank 1. VLM lightmap array BL_L_L20 with DT1_1, DT1_2, DT1_3, Inserts, Parts, Playfield primitives.
- `games/warlok.json#/lamps/18._note`: Playfield insert lamp near Drop Target Bank 2. VLM lightmap array BL_L_L21 with DT2_1, DT2_2, DT2_3, Inserts, Parts, Playfield primitives.
- `games/warlok.json#/lamps/19._note`: Playfield insert lamp near Drop Target Bank 3. VLM lightmap array BL_L_L22 with DT3_1, DT3_2, DT3_3, Inserts, Parts, Playfield primitives.
- `games/warlok.json#/lamps/20._note`: Playfield insert lamp. VLM lightmap array BL_L_L23 with DT1_2, Inserts, Parts, Playfield primitives.
- `games/warlok.json#/lamps/21._note`: Playfield insert lamp. VLM lightmap array BL_L_L24 with DT2_1, DT2_2, DT2_3, Inserts, Parts, Playfield primitives.
- `games/warlok.json#/lamps/22._note`: Playfield insert lamp near Bumper 2. VLM lightmap array BL_L_L25 with BR2, Bumper2Skirt, DT3_1, DT3_2, DT3_3, Inserts, Parts, Playfield primitives.
- `games/warlok.json#/lamps/23._note`: Playfield insert lamp. VLM lightmap array BL_L_L26 with Inserts, Parts, Playfield primitives.
- `games/warlok.json#/lamps/24._note`: Playfield insert lamp. VLM lightmap array BL_L_L27 with Inserts, Parts, Playfield primitives.
- `games/warlok.json#/lamps/25._note`: Playfield insert lamp. VLM lightmap array BL_L_L28 with Inserts, Parts, Playfield primitives.
- `games/warlok.json#/lamps/26._note`: Playfield insert lamp. VLM lightmap array BL_L_L29 with Inserts, Parts, Playfield primitives.
- `games/warlok.json#/lamps/27._note`: Playfield insert lamp. VLM lightmap array BL_L_L30 with Inserts, Parts, Playfield primitives.
- `games/warlok.json#/lamps/28._note`: Playfield insert lamp near left flipper. VLM lightmap array BL_L_L31 with FlipperL, FlipperLup, Inserts, LSling1, LSling2, Parts, Playfield primitives.
- `games/warlok.json#/lamps/29._note`: Playfield insert lamp. VLM lightmap array BL_L_L32 with Inserts, Parts, Playfield primitives.
- `games/warlok.json#/lamps/30._note`: Playfield insert lamp. VLM lightmap array BL_L_L33 with Inserts, Parts, Playfield primitives.
- `games/warlok.json#/lamps/31._note`: Playfield insert lamp near flippers. VLM lightmap array BL_L_L34 with FlipperLup, FlipperR, FlipperRup, Inserts, Parts, Playfield primitives.
- `games/warlok.json#/lamps/32._note`: Playfield insert lamp. VLM lightmap array BL_L_L35 with Gate_5, Inserts, Parts, Playfield primitives.
- `games/warlok.json#/lamps/33._note`: Playfield insert lamp. VLM lightmap array BL_L_L36 with Inserts, Parts, Playfield primitives.
- `games/warlok.json#/lamps/34._note`: Playfield insert lamp. VLM lightmap array BL_L_L37 with Inserts, Parts, Playfield primitives.
- `games/warlok.json#/lamps/35._note`: Playfield insert lamp. VLM lightmap array BL_L_L38 with Inserts, Parts, Playfield, RSling, RSling1, RSling2 primitives.
- `games/warlok.json#/lamps/36._note`: Playfield insert lamp near Bumper 1. VLM lightmap array BL_L_L39 with BR1, Bumper1Skirt, HT, Inserts, Parts, Playfield primitives.
- `games/warlok.json#/lamps/37._note`: Playfield insert lamp near left slingshot. VLM lightmap array BL_L_L40 with Inserts, LSling, LSling1, LSling2, Parts, Playfield primitives.
- `games/warlok.json#/lamps/38._note`: Playfield insert lamp near left slingshot. VLM lightmap array BL_L_L41 with Inserts, LSling, LSling1, LSling2, Parts, Playfield primitives.
- `games/warlok.json#/lamps/39._note`: Playfield insert lamp. VLM lightmap array BL_L_L42 with Inserts, Parts, Playfield primitives.
- `games/warlok.json#/lamps/40._note`: Playfield insert lamp. VLM lightmap array BL_L_L43 with Inserts, Parts, Playfield primitives.
- `games/warlok.json#/lamps/41._note`: Playfield insert lamp. VLM lightmap array BL_L_L44 with Inserts, Parts, Playfield primitives.
- `games/warlok.json#/lamps/42._note`: Playfield insert lamp. VLM lightmap array BL_L_L45 with Inserts, Playfield primitives.
- `games/warlok.json#/lamps/43._note`: Playfield insert lamp. VLM lightmap array BL_L_L46 with Inserts, Parts, Playfield primitives.
- `games/warlok.json#/lamps/44._note`: Playfield insert lamp near right slingshot. VLM lightmap array BL_L_L47 with Inserts, Parts, Playfield, RSling, RSling1, RSling2 primitives.
- `games/warlok.json#/lamps/45._note`: Playfield insert lamp near left slingshot. VLM lightmap array BL_L_L49 with Inserts, LSling, LSling1, LSling2, Parts, Playfield primitives.
- `games/warlok.json#/lamps/46._note`: Playfield insert lamp. VLM lightmap array BL_L_L50 with Inserts, Parts, Playfield primitives.
- `games/warlok.json#/lamps/47._note`: Playfield insert lamp. VLM lightmap array BL_L_L51 with Inserts, Parts, Playfield primitives.
- `games/warlok.json#/lamps/48._note`: Playfield insert lamp. VLM lightmap array BL_L_L52 with Inserts, Parts, Playfield primitives.
- `games/warlok.json#/lamps/49._note`: Playfield insert lamp. VLM lightmap array BL_L_L53 with Inserts, Parts, Playfield primitives.
- `games/warlok.json#/lamps/50._note`: Playfield insert lamp. VLM lightmap array BL_L_L54 with Inserts, Parts, Playfield primitives.
- `games/warlok.json#/lamps/51._note`: Playfield insert lamp near right slingshot. VLM lightmap array BL_L_L55 with Inserts, Parts, Playfield, RSling, RSling1, RSling2 primitives.
- `games/warlok.json#/lamps/52._note`: Playfield insert lamp near left slingshot. VLM lightmap array BL_L_L57 with Inserts, LSling, LSling1, LSling2, Playfield primitives.
- `games/warlok.json#/lamps/53._note`: Playfield insert lamp. VLM lightmap array BL_L_L58 with Inserts, Playfield primitives.
- `games/warlok.json#/lamps/54._note`: Playfield insert lamp near right flipper. VLM lightmap array BL_L_L59 with FlipperR, Inserts, Parts, Playfield primitives.
- `games/warlok.json#/lamps/55._note`: Playfield insert lamp. VLM lightmap array BL_L_L60 with Inserts, Parts, Playfield primitives.
- `games/warlok.json#/lamps/56._note`: Playfield insert lamp. VLM lightmap array BL_L_L61 with Inserts, Parts, Playfield primitives.
- `games/warlok.json#/lamps/57._note`: Playfield insert lamp. VLM lightmap array BL_L_L62 with Inserts, Parts, Playfield primitives.
- `games/warlok.json#/lamps/58._note`: Playfield insert lamp. VLM lightmap array BL_L_L63 with Inserts, Parts, Playfield, RSling2 primitives.
- `games/warlok.json#/_source/confidence_notes`: High confidence extraction from VPW VBScript. Platform identified as Williams System 7 via LoadVPM '01560000', 'S7.VBS', 3.26. ROM name 'wrlok_l3' from cGameName constant. This is an early-80s EM/SS hybrid era table with no traditional trough — instead uses a single Drain kicker (VPX object 'Drain') with Controller.Switch(9) set on Drain_Hit/Drain_UnHit and SolCallback(4)='SolRelease' which kicks the ball out with Drain.kick(66,20). Ball is pre-created on the Drain object at table init (Drain.Createball / Controller.Switch(9)=1). No bsTrough or cvpmBallStack objects used — this is a simple single-ball drain-and-release pattern typical of System 7 era. Switches identified from Controller.Switch on/off pairs (drain sw9, wire triggers sw16-18/23-26, rollunder gates sw22/37/38, flipper button sw36), PulseSw calls (spinners sw10-12, bumpers sw13-15, standup target sw19, slingshots sw20-21), and DTHit calls (drop targets sw27-35 across three banks). Solenoids 1-3 are drop target bank resets (Sol1DropUp resets sw27-29, Sol2DropUp resets sw30-32, Sol3DropUp resets sw33-35). Solenoids 5-7 are individual drop target actuators (dt1drop/dt2drop/dt3drop raise sw33/34/35). Sol 8 is GI relay with inverted logic (enabled=GI off, per MetaTed hack fix comment for orbit shot). Sol 15 is knocker. Sol 23 is game-on relay via vpmNudge.SolGameOn. Flipper solenoids use S7.VBS framework constants sLRFlipper=14 and sLLFlipper=16. Lamps mapped via vpmMapLights AllLamps using VPX light TimerInterval values — lamp IDs 8-63 (with gaps at 48, 56) identified from BL_L_L* VLM lightmap arrays. Six backglass indicator lamps (2,3,4,5,6,15) driven by LampCallback/UpdateMultipleLamps reading Controller.Lamp() and setting gi25-gi30 VPX objects. GI controlled by Sol 8 with inverted behavior. Switch 36 is right flipper cabinet button, set via Controller.Switch(36) on RightFlipperKey press/release — unusual for S7 where cabinet switches are typically ROM-managed, but this appears to be a VPW implementation choice for the flipper EOS or lane change feature.

## Unresolved questions

- Is the I/O enumeration complete for every supported physical/controller variant?
- Which inferred VPX behaviors reflect real hardware, and which are table-script conveniences?
- Are all mechanism home states, sensors, motion constraints, and ball interactions documented?

## Sources

- `legacy.game.warlok`: `games/warlok.json` at the pinned migration revision.
