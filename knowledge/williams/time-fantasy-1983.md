# Time Fantasy

Coverage: **partial - source-derived recreation knowledge requiring validation**

## Overview

Legacy evidence identifies this candidate as Williams (1983). The information below is preserved for recreation work but is not automatically treated as validated physical-machine fact.

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

- `games/time-fantasy.json#/switches/0._note`: vpmNudge.TiltSwitch=1. Standard tilt switch.
- `games/time-fantasy.json#/switches/1._note`: STHit 9. VPW TargetBouncer standup target with BM_sw9 primitive animation. Part of 8-target set (sw9-sw15, sw36).
- `games/time-fantasy.json#/switches/2._note`: STHit 10. VPW TargetBouncer standup target with BM_sw10 primitive.
- `games/time-fantasy.json#/switches/3._note`: STHit 11. VPW TargetBouncer standup target with BM_sw11 primitive.
- `games/time-fantasy.json#/switches/4._note`: STHit 12. VPW TargetBouncer standup target with BM_sw12 primitive.
- `games/time-fantasy.json#/switches/5._note`: STHit 13. VPW TargetBouncer standup target with BM_sw13 primitive.
- `games/time-fantasy.json#/switches/6._note`: STHit 14. VPW TargetBouncer standup target with BM_sw14 primitive.
- `games/time-fantasy.json#/switches/7._note`: STHit 15. VPW TargetBouncer standup target with BM_sw15 primitive.
- `games/time-fantasy.json#/switches/8._note`: Controller.Switch(16) on/off. Wire trigger with AnimateWire animation (BP_sw16 drops 13 units on hit).
- `games/time-fantasy.json#/switches/9._note`: Controller.Switch(17) on/off. Wire trigger with AnimateWire animation.
- `games/time-fantasy.json#/switches/10._note`: Controller.Switch(18) on/off. Wire trigger with AnimateWire animation. Illuminated by GI029 and GI032 split zones.
- `games/time-fantasy.json#/switches/11._note`: Controller.Switch(19) on/off. Wire trigger with AnimateWire animation. Illuminated by GI029 split zone.
- `games/time-fantasy.json#/switches/12._note`: Controller.Switch(20) on/off. Wire trigger with AnimateWire. Calls leftInlaneSpeedLimit on hit. Illuminated by GI029 and GI032 split zones.
- `games/time-fantasy.json#/switches/13._note`: Controller.Switch(21) on/off. Wire trigger with AnimateWire. Calls rightInlaneSpeedLimit on hit. Illuminated by GI029 split zone.
- `games/time-fantasy.json#/switches/14._note`: Controller.Switch(22) on/off. Wire trigger with AnimateWire animation.
- `games/time-fantasy.json#/switches/15._note`: Controller.Switch(23) on/off. Wire trigger with AnimateWire animation.
- `games/time-fantasy.json#/switches/16._note`: Controller.Switch(24) on/off. Wire trigger with AnimateWire animation.
- `games/time-fantasy.json#/switches/17._note`: Controller.Switch(25) on/off. Wire trigger with AnimateWire animation.
- `games/time-fantasy.json#/switches/18._note`: Controller.Switch(26) on/off. Wire trigger with AnimateWire animation.
- `games/time-fantasy.json#/switches/19._note`: PulseSw 27. Scoring rubber with SlingF animation (3 visual frames). Lower hit threshold (LowerRubberHitThreshold=2). Illuminated by GI032 and GI033 split zones.
- `games/time-fantasy.json#/switches/20._note`: PulseSw 28. Scoring rubber with SlingA animation (3 visual frames). Upper hit threshold (UpperRubberHitThreshold=4). Debug prints 'A final speed'.
- `games/time-fantasy.json#/switches/21._note`: PulseSw 29. Scoring rubber with SlingB animation (3 visual frames). Same upper threshold as sw28. Debug prints 'B final speed'.
- `games/time-fantasy.json#/switches/22._note`: PulseSw 30. Scoring rubber with SlingC animation (3 visual frames). Lower hit threshold.
- `games/time-fantasy.json#/switches/23._note`: PulseSw 31. Scoring rubber with SlingD animation (3 visual frames). Lower hit threshold.
- `games/time-fantasy.json#/switches/24._note`: PulseSw 32. Scoring rubber with SlingE animation (3 visual frames). Lower hit threshold. Illuminated by GI028 and GI029 split zones.
- `games/time-fantasy.json#/switches/25._note`: PulseSw 33. Bumper3_Hit. Bumper with skirt tilt animation (BP_Bumper_Skirt_001). RandomSoundBumperTop.
- `games/time-fantasy.json#/switches/26._note`: PulseSw 34. Bumper2_Hit. Bumper with skirt tilt animation (BP_Bumper_Skirt_002). RandomSoundBumperMiddle.
- `games/time-fantasy.json#/switches/27._note`: PulseSw 35. Bumper1_Hit. Bumper with skirt tilt animation (BP_Bumper_Socket). RandomSoundBumperBottom.
- `games/time-fantasy.json#/switches/28._note`: STHit 36. VPW TargetBouncer standup target with BM_sw36 primitive. The 8th target in the set (sw9-sw15 plus sw36).
- `games/time-fantasy.json#/switches/29._note`: PulseSw 37. LeftSlingShot_Slingshot event. Uses SlingshotCorrection (LS object). Animated with BP_LSling frames. RandomSoundSlingshotLeft.
- `games/time-fantasy.json#/switches/30._note`: PulseSw 38. RightSlingShot_Slingshot event. Uses SlingshotCorrection (RS object). Animated with BP_RSling frames. RandomSoundSlingshotRight.
- `games/time-fantasy.json#/switches/31._note`: Controller.Switch(39)=1 on Drain_Hit, =0 on Drain_UnHit. Single-ball trough — ball created in Drain kicker at init. Controller.Switch(39)=1 also set in Table1_Init. SolRelease (sol 1) kicks ball out.
- `games/time-fantasy.json#/switches/32._note`: PulseSw 40 fired inside SolRFlipper when flipper is activated (enabled=True). Not a physical switch object — pulsed by code on every right flipper fire. Likely used by ROM for end-of-stroke detection.
- `games/time-fantasy.json#/switches/33._note`: Controller.Switch(42) on/off. Wire trigger with AnimateWire animation.
- `games/time-fantasy.json#/coils/0._vbscript_callback`: SolRelease
- `games/time-fantasy.json#/coils/0._inferred_type`: ball_management
- `games/time-fantasy.json#/coils/0._note`: Kicks ball from Drain kicker. Drain.kick 60,15. Single-ball system — no multi-ball trough. Ball is created in Drain at table init.
- `games/time-fantasy.json#/coils/1._vbscript_callback`: SetRelayGI
- `games/time-fantasy.json#/coils/1._inferred_type`: mechanism
- `games/time-fantasy.json#/coils/1._note`: GI Relay — INVERTED. When aLvl=0, GI turns ON (bulb.State=1 for all GI lights). When aLvl=1 (enabled), GI turns OFF. Four GI split zones in VLM: GI028, GI029, GI032, GI033. S7-era single GI relay controlling all zones simultaneously.
- `games/time-fantasy.json#/coils/2._vbscript_callback`: KnockerSolenoid
- `games/time-fantasy.json#/coils/2._inferred_type`: knocker
- `games/time-fantasy.json#/coils/2._note`: SolCallback has trailing apostrophe commenting out the callback name ('KnockerSolenoid'') — but the Sub KnockerSolenoid() exists and plays 'Bell' sound via SoundFX('Bell',DOFKnocker). Comment says 'Repurposed for bell sound'. On the real machine this was likely the bell solenoid.
- `games/time-fantasy.json#/coils/3._vbscript_callback`: BackglassLit
- `games/time-fantasy.json#/coils/3._inferred_type`: mechanism
- `games/time-fantasy.json#/coils/3._note`: Controls VR backglass illumination (VR_BGLit visibility). Only active in VR mode. On the real machine this likely controlled a backglass illumination relay.
- `games/time-fantasy.json#/lamps/0._note`: Controller.Lamp(1) checked in UpdateTextBoxes/UpdateVRLamps. Shows 'KEEP_SHOOTING' text / KeepShootingReel. Same Player Shoots Again indicator.
- `games/time-fantasy.json#/lamps/1._note`: Controller.Lamp(2) checked in UpdateTextBoxes/UpdateVRLamps. Shows 'BIP' text / BIPReel.
- `games/time-fantasy.json#/lamps/2._note`: Controller.Lamp(3) checked in UpdateTextBoxes/UpdateVRLamps. Shows 'TILT' text / TiltReel.
- `games/time-fantasy.json#/lamps/3._note`: Controller.Lamp(4) checked in UpdateTextBoxes/UpdateVRLamps. Shows 'GAME_OVER' text / GameOverReel.
- `games/time-fantasy.json#/lamps/4._note`: Controller.Lamp(5) checked in UpdateTextBoxes/UpdateVRLamps. Shows 'MATCH' text / MatchReel.
- `games/time-fantasy.json#/lamps/5._note`: VLM baked lighting array BL_L_L7 present. vpmMapLights AllLamps assigns via TimerInterval.
- `games/time-fantasy.json#/lamps/6._note`: VLM baked lighting array BL_L_L8 present (illuminates PostCenter). vpmMapLights AllLamps.
- `games/time-fantasy.json#/lamps/7._note`: VLM baked lighting array BL_L_L9 present. vpmMapLights AllLamps.
- `games/time-fantasy.json#/lamps/8._note`: VLM baked lighting array BL_L_L10 present (illuminates area around sw9 standup target). vpmMapLights AllLamps.
- `games/time-fantasy.json#/lamps/9._note`: VLM baked lighting array BL_L_L11 present (illuminates area around sw10 standup target). vpmMapLights AllLamps.
- `games/time-fantasy.json#/lamps/10._note`: VLM baked lighting array BL_L_L12 present (illuminates area around sw12). vpmMapLights AllLamps.
- `games/time-fantasy.json#/lamps/11._note`: VLM baked lighting array BL_L_L13 present (illuminates area around sw12/sw13). vpmMapLights AllLamps.
- `games/time-fantasy.json#/lamps/12._note`: VLM baked lighting array BL_L_L14 present (illuminates area around sw14). vpmMapLights AllLamps.
- `games/time-fantasy.json#/lamps/13._note`: VLM baked lighting array BL_L_L15 present (illuminates area around sw15). vpmMapLights AllLamps.
- `games/time-fantasy.json#/lamps/14._note`: VLM baked lighting array BL_L_L16 present. vpmMapLights AllLamps.
- `games/time-fantasy.json#/lamps/15._note`: VLM baked lighting array BL_L_L17 present. vpmMapLights AllLamps.
- `games/time-fantasy.json#/lamps/16._note`: VLM baked lighting array BL_L_L18 present. vpmMapLights AllLamps.
- `games/time-fantasy.json#/lamps/17._note`: VLM baked lighting array BL_L_L19 present. vpmMapLights AllLamps.
- `games/time-fantasy.json#/lamps/18._note`: VLM baked lighting array BL_L_L20 present. Opacity doubled at init (BL_L_L20 opacity * 2). vpmMapLights AllLamps.
- `games/time-fantasy.json#/lamps/19._note`: VLM baked lighting array BL_L_L21 present (also illuminates RSling area). Opacity doubled at init. vpmMapLights AllLamps.
- `games/time-fantasy.json#/lamps/20._note`: VLM baked lighting array BL_L_L22 present. vpmMapLights AllLamps.
- `games/time-fantasy.json#/lamps/21._note`: VLM baked lighting array BL_L_L23 present. vpmMapLights AllLamps.
- `games/time-fantasy.json#/lamps/22._note`: VLM baked lighting array BL_L_L24 present. vpmMapLights AllLamps.
- `games/time-fantasy.json#/lamps/23._note`: VLM baked lighting array BL_L_L25 present. vpmMapLights AllLamps.
- `games/time-fantasy.json#/lamps/24._note`: VLM baked lighting array BL_L_L26 present. vpmMapLights AllLamps.
- `games/time-fantasy.json#/lamps/25._note`: VLM baked lighting array BL_L_L27 present. vpmMapLights AllLamps.
- `games/time-fantasy.json#/lamps/26._note`: VLM baked lighting array BL_L_L28 present. vpmMapLights AllLamps.
- `games/time-fantasy.json#/lamps/27._note`: VLM baked lighting array BL_L_L29 present. vpmMapLights AllLamps.
- `games/time-fantasy.json#/lamps/28._note`: VLM baked lighting array BL_L_L30 present. vpmMapLights AllLamps.
- `games/time-fantasy.json#/lamps/29._note`: VLM baked lighting array BL_L_L31 present. vpmMapLights AllLamps.
- `games/time-fantasy.json#/lamps/30._note`: VLM baked lighting array BL_L_L32 present. vpmMapLights AllLamps.
- `games/time-fantasy.json#/lamps/31._note`: VLM baked lighting array BL_L_L33 present. vpmMapLights AllLamps.
- `games/time-fantasy.json#/lamps/32._note`: VLM baked lighting array BL_L_L34 present. vpmMapLights AllLamps.
- `games/time-fantasy.json#/lamps/33._note`: VLM baked lighting array BL_L_L35 present. vpmMapLights AllLamps.
- `games/time-fantasy.json#/lamps/34._note`: VLM baked lighting array BL_L_L36 present. vpmMapLights AllLamps.
- `games/time-fantasy.json#/lamps/35._note`: VLM baked lighting array BL_L_L37 present. vpmMapLights AllLamps.
- `games/time-fantasy.json#/lamps/36._note`: VLM baked lighting array BL_L_L38 present. vpmMapLights AllLamps.
- `games/time-fantasy.json#/lamps/37._note`: VLM baked lighting array BL_L_L39 present. vpmMapLights AllLamps.
- `games/time-fantasy.json#/lamps/38._note`: VLM baked lighting array BL_L_L40 present. vpmMapLights AllLamps.
- `games/time-fantasy.json#/lamps/39._note`: VLM baked lighting array BL_L_L41 present. vpmMapLights AllLamps.
- `games/time-fantasy.json#/lamps/40._note`: VLM baked lighting array BL_L_L42 present. vpmMapLights AllLamps.
- `games/time-fantasy.json#/lamps/41._note`: VLM baked lighting array BL_L_L43 present. vpmMapLights AllLamps.
- `games/time-fantasy.json#/lamps/42._note`: VLM baked lighting array BL_L_L44 present. vpmMapLights AllLamps.
- `games/time-fantasy.json#/lamps/43._note`: VLM baked lighting array BL_L_L45 present. vpmMapLights AllLamps.
- `games/time-fantasy.json#/lamps/44._note`: VLM baked lighting array BL_L_L46 present. vpmMapLights AllLamps.
- `games/time-fantasy.json#/lamps/45._note`: VLM baked lighting array BL_L_L47 present. vpmMapLights AllLamps.
- `games/time-fantasy.json#/lamps/46._note`: VLM baked lighting array BL_L_L48 present. vpmMapLights AllLamps.
- `games/time-fantasy.json#/lamps/47._note`: VLM baked lighting array BL_L_L49 present. vpmMapLights AllLamps.
- `games/time-fantasy.json#/lamps/48._note`: VLM baked lighting array BL_L_L50 present. vpmMapLights AllLamps.
- `games/time-fantasy.json#/lamps/49._note`: VLM baked lighting array BL_L_L51 present. vpmMapLights AllLamps.
- `games/time-fantasy.json#/lamps/50._note`: VLM baked lighting array BL_L_L52 present. vpmMapLights AllLamps.
- `games/time-fantasy.json#/lamps/51._note`: VLM baked lighting array BL_L_L53 present. vpmMapLights AllLamps.
- `games/time-fantasy.json#/lamps/52._note`: VLM baked lighting array BL_L_L54 present. vpmMapLights AllLamps.
- `games/time-fantasy.json#/lamps/53._note`: VLM baked lighting array BL_L_L55 present. vpmMapLights AllLamps.
- `games/time-fantasy.json#/lamps/54._note`: VLM baked lighting array BL_L_L56 present. vpmMapLights AllLamps.
- `games/time-fantasy.json#/lamps/55._note`: VLM baked lighting array BL_L_L57 present. vpmMapLights AllLamps.
- `games/time-fantasy.json#/lamps/56._note`: VLM baked lighting array BL_L_L58 present. vpmMapLights AllLamps.
- `games/time-fantasy.json#/lamps/57._note`: VLM baked lighting array BL_L_L59 present. vpmMapLights AllLamps.
- `games/time-fantasy.json#/lamps/58._note`: VLM baked lighting array BL_L_L60 present (illuminates left flipper area / FlipperLup). vpmMapLights AllLamps.
- `games/time-fantasy.json#/lamps/59._note`: VLM baked lighting array BL_L_L61 present. vpmMapLights AllLamps.
- `games/time-fantasy.json#/lamps/60._note`: VLM baked lighting array BL_L_L62 present (illuminates right flipper area / FlipperRup). vpmMapLights AllLamps.
- `games/time-fantasy.json#/lamps/61._note`: VLM baked lighting array BL_L_L63 present (illuminates right flipper area / FlipperRup). vpmMapLights AllLamps.
- `games/time-fantasy.json#/lamps/62._note`: VLM baked lighting array BL_L_l64 present. vpmMapLights AllLamps.
- `games/time-fantasy.json#/_source/confidence_notes`: High confidence extraction from VPW v1.0 by mcarter78/apophis. Platform is Williams System 7 (s7.vbs loaded via LoadVPM). ROM is tmfnt_l5. This is a single-ball game (tnob=1, lob=0) with no traditional multi-ball trough — the drain is a simple kicker (VPX object 'Drain') that holds one ball. Controller.Switch(39)=1 is set on init and on Drain_Hit; SolRelease (sol 1) kicks the ball back into play via Drain.kick. No bsTrough/cvpmTrough framework is used. Switches identified from Controller.Switch on/off pairs (sw16-sw26, sw42 — wire triggers with AnimateWire), PulseSw calls (sw27-sw32 — scoring rubbers with SlingA-F animation, sw33-sw35 — bumpers, sw37-sw38 — slingshots, sw40 — right flipper EOS pulsed in SolRFlipper), and STHit standup target system (sw9-sw15, sw36 — 8 standup targets using VPW TargetBouncer with animate/physics). Lamps use vpmMapLights AllLamps (UseLamps=1) — VPX light objects have TimerInterval set to lamp number. VLM baked lighting arrays confirm lamp IDs 7-64 from BL_L_L* definitions. Backglass lamps 1-5 are read via Controller.Lamp in UpdateTextBoxes/UpdateVRLamps (1=Keep Shooting, 2=Ball In Play, 3=Tilt, 4=Game Over, 5=Match). GI is controlled by sol 11 via SetRelayGI — INVERTED logic (aLvl=0 turns GI ON). Four GI split zones identified from VLM arrays: GI028, GI029, GI032, GI033. Sol 25 drives BackglassLit for VR backglass illumination. Sol 15 is KnockerSolenoid but repurposed for bell sound (comment says 'Repurposed for bell sound'). No cvpmMech, no diverters, no drop targets, no ramp diverters found.

## Unresolved questions

- Is the I/O enumeration complete for every supported physical/controller variant?
- Which inferred VPX behaviors reflect real hardware, and which are table-script conveniences?
- Are all mechanism home states, sensors, motion constraints, and ball interactions documented?

## Sources

- `legacy.game.time-fantasy`: `games/time-fantasy.json` at the pinned migration revision.
