# Skateball

Coverage: **partial - source-derived recreation knowledge requiring validation**

## Overview

Legacy evidence identifies this candidate as Bally (1980). The information below is preserved for recreation work but is not automatically treated as validated physical-machine fact.

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
- `games/skateball.json#/switches/0._note`: vpmNudge.TiltSwitch = swTilt. Bally.vbs framework constant swTilt = 1.
- `games/skateball.json#/switches/1._note`: DTHit 2. Center bank of 3 drop targets (sw2, sw3, sw4). Reset by solenoid 10 (DTBankCenterReset).
- `games/skateball.json#/switches/2._note`: DTHit 3. Center bank of 3 drop targets.
- `games/skateball.json#/switches/3._note`: DTHit 4. Center bank of 3 drop targets.
- `games/skateball.json#/switches/4._note`: Controller.Switch(5) = 1 on hit, cleared by SolKicker (solenoid 2). SoundSaucerLock on entry. DIP switches reference 'saucer extra ball' feature.
- `games/skateball.json#/switches/5._note`: Controller.Switch(8) = 1/0 on Drain_Hit/Drain_UnHit. Single-ball outhole design. Ball created in Drain at table init with Controller.Switch(8) = 1. SolBallRelease (sol 7) kicks and clears.
- `games/skateball.json#/switches/6._note`: PulseSw 13. Has animated VLM trigger object (BP_sw13). Located in upper playfield area near bumpers.
- `games/skateball.json#/switches/7._note`: PulseSw 14. Has animated VLM trigger object (BP_sw14). Located in upper playfield area near bumpers.
- `games/skateball.json#/switches/8._note`: PulseSw 15. Has animated VLM trigger object (BP_sw15). Located in upper playfield area.
- `games/skateball.json#/switches/9._note`: PulseSw 17. Seven VPX trigger objects (sw17a through sw17g) all pulse switch 17. Top lane scoring rubbers.
- `games/skateball.json#/switches/10._note`: PulseSw 18. Has animated VLM trigger object (BP_sw18).
- `games/skateball.json#/switches/11._note`: PulseSw 19. Has animated VLM trigger object (BP_sw19).
- `games/skateball.json#/switches/12._note`: DTHit 20. Left bank of 5 drop targets (sw20-24). Reset by solenoid 8 (DTBankLeftReset).
- `games/skateball.json#/switches/13._note`: DTHit 21. Left bank of 5 drop targets.
- `games/skateball.json#/switches/14._note`: DTHit 22. Left bank of 5 drop targets.
- `games/skateball.json#/switches/15._note`: DTHit 23. Left bank of 5 drop targets.
- `games/skateball.json#/switches/16._note`: DTHit 24. Left bank of 5 drop targets.
- `games/skateball.json#/switches/17._note`: DTHit 26. Top bank of 3 drop targets (sw26-28). Reset by solenoid 9 (DTBankTopReset).
- `games/skateball.json#/switches/18._note`: DTHit 27. Top bank of 3 drop targets.
- `games/skateball.json#/switches/19._note`: DTHit 28. Top bank of 3 drop targets.
- `games/skateball.json#/switches/20._note`: PulseSw 30. Has animated VLM star rollover object (BP_Star_sw30).
- `games/skateball.json#/switches/21._note`: PulseSw 31. Has animated VLM star rollover object (BP_Star_sw31).
- `games/skateball.json#/switches/22._note`: Controller.Switch(32) = 1 on RightFlipperKey KeyDown, cleared on KeyUp. Used by ROM for lane change or similar feature. Not a physical playfield switch -- triggered by cabinet button.
- `games/skateball.json#/switches/23._note`: PulseSw 33 from sw33_Spin event. Elaborate VLM spinner animation with inner/outer russian doll opacity crossfade and rod rotation.
- `games/skateball.json#/switches/24._note`: PulseSw 34. Has animated VLM trigger object (BP_sw34).
- `games/skateball.json#/switches/25._note`: PulseSw 35. Has animated VLM trigger object (BP_sw35).
- `games/skateball.json#/switches/26._note`: PulseSw 36 from RightSlingShot_Slingshot event. Has 4-frame VLM sling animation (BP_RightSling1-4) and mechanical arm rotation (BP_remk).
- `games/skateball.json#/switches/27._note`: PulseSw 37 from LeftSlingShot_Slingshot event. Has 4-frame VLM sling animation (BP_LeftSling1-4) and mechanical arm rotation (BP_lemk).
- `games/skateball.json#/switches/28._note`: PulseSw 38 from Bumper2_Hit. Has animated ring (BP_Bumper2_Ring) and skirt.
- `games/skateball.json#/switches/29._note`: PulseSw 39 from Bumper3_Hit. Has animated ring (BP_Bumper3_Ring) and skirt.
- `games/skateball.json#/switches/30._note`: PulseSw 40 from Bumper1_Hit. Has animated ring (BP_Bumper1_Ring) and skirt.
- `games/skateball.json#/coils/0._vbscript_callback`: SolKicker
- `games/skateball.json#/coils/0._inferred_type`: ball_management
- `games/skateball.json#/coils/0._note`: Kicks ball from saucer (sw5). sw5.kick 197+rnd*0.5, 20. Clears Controller.Switch(5).
- `games/skateball.json#/coils/1._vbscript_callback`: vpmSolSound SoundFX("fx_knocker",DOFKnocker),
- `games/skateball.json#/coils/1._inferred_type`: knocker
- `games/skateball.json#/coils/1._note`: Cabinet knocker solenoid. Sound-only callback via vpmSolSound.
- `games/skateball.json#/coils/2._vbscript_callback`: SolBallRelease
- `games/skateball.json#/coils/2._inferred_type`: ball_management
- `games/skateball.json#/coils/2._note`: Kicks ball from Drain kicker. Drain.kick 57, 20. Clears Controller.Switch(8). Single-ball outhole design.
- `games/skateball.json#/coils/3._vbscript_callback`: DTBankLeftReset
- `games/skateball.json#/coils/3._inferred_type`: drop_target_reset
- `games/skateball.json#/coils/3._note`: Resets left bank of 5 drop targets (sw20, sw21, sw22, sw23, sw24). Uses DTRaise for each target.
- `games/skateball.json#/coils/4._vbscript_callback`: DTBankTopReset
- `games/skateball.json#/coils/4._inferred_type`: drop_target_reset
- `games/skateball.json#/coils/4._note`: Resets top bank of 3 drop targets (sw26, sw27, sw28). Uses DTRaise for each target.
- `games/skateball.json#/coils/5._vbscript_callback`: DTBankCenterReset
- `games/skateball.json#/coils/5._inferred_type`: drop_target_reset
- `games/skateball.json#/coils/5._note`: Resets center bank of 3 drop targets (sw2, sw3, sw4). Uses DTRaise for each target.
- `games/skateball.json#/coils/6._vbscript_callback`: SolRFlipper
- `games/skateball.json#/coils/6._inferred_type`: flipper
- `games/skateball.json#/coils/6._note`: sLRFlipper = 17 (Bally.vbs framework constant). nFozzy flipper implementation: RF.Fire on enable, RightFlipper.RotateToStart on disable.
- `games/skateball.json#/coils/7._vbscript_callback`: SolLFlipper
- `games/skateball.json#/coils/7._inferred_type`: flipper
- `games/skateball.json#/coils/7._note`: sLLFlipper = 18 (Bally.vbs framework constant). nFozzy flipper implementation: LF.Fire on enable, LeftFlipper.RotateToStart on disable.
- `games/skateball.json#/coils/8._vbscript_callback`: SolRFlipper1
- `games/skateball.json#/coils/8._inferred_type`: flipper
- `games/skateball.json#/coils/8._note`: sURFlipper = 19 (Bally.vbs framework constant). nFozzy flipper implementation: URF.Fire on enable, RightFlipper1.RotateToStart on disable.
- `games/skateball.json#/coils/9._vbscript_callback`: SolLFlipper1
- `games/skateball.json#/coils/9._inferred_type`: flipper
- `games/skateball.json#/coils/9._note`: sULFlipper = 20 (Bally.vbs framework constant). nFozzy flipper implementation: ULF.Fire on enable, LeftFlipper1.RotateToStart on disable.
- `games/skateball.json#/coils/10._vbscript_callback`: vpmNudge.SolGameOn
- `games/skateball.json#/coils/10._inferred_type`: mechanism
- `games/skateball.json#/coils/10._note`: Game On relay. Standard Bally framework solenoid handled by vpmNudge.SolGameOn.
- `games/skateball.json#/lamps/0._note`: VLM lightmap: BL_L_l1 (Playfield)
- `games/skateball.json#/lamps/1._note`: VLM lightmap: BL_L_l2 (Playfield)
- `games/skateball.json#/lamps/2._note`: VLM lightmap: BL_L_l3 (Playfield)
- `games/skateball.json#/lamps/3._note`: VLM lightmap: BL_L_l4 (Playfield)
- `games/skateball.json#/lamps/4._note`: VLM lightmap: BL_L_l5 (Playfield)
- `games/skateball.json#/lamps/5._note`: VLM lightmap: BL_L_l6 (Parts, Playfield)
- `games/skateball.json#/lamps/6._note`: VLM lightmap: BL_L_l7 (Playfield, RFlipper1U). Near upper right flipper.
- `games/skateball.json#/lamps/7._note`: VLM lightmap: BL_L_l8 (Parts, Plastics, Playfield)
- `games/skateball.json#/lamps/8._note`: VLM lightmap: BL_L_l9 (Parts, Playfield)
- `games/skateball.json#/lamps/9._note`: VLM lightmap: BL_L_l10 (Bumper1_Ring, Playfield). Near top bumper.
- `games/skateball.json#/lamps/10._note`: VLM lightmap: BL_L_l12 (Parts, Playfield)
- `games/skateball.json#/lamps/11._note`: Backglass lamp. UpdateMultipleLamps: Controller.Lamp(13) drives FlBGL13 opacity. Comment: 'Ball In Play'.
- `games/skateball.json#/lamps/12._note`: VLM lightmap: BL_L_l14 (Playfield)
- `games/skateball.json#/lamps/13._note`: VLM lightmap: BL_L_l15 (Playfield)
- `games/skateball.json#/lamps/14._note`: VLM lightmap: BL_L_l17 (Playfield, RFlipperU). Near lower right flipper.
- `games/skateball.json#/lamps/15._note`: VLM lightmap: BL_L_l18 (Playfield)
- `games/skateball.json#/lamps/16._note`: VLM lightmap: BL_L_l19 (Playfield)
- `games/skateball.json#/lamps/17._note`: VLM lightmap: BL_L_l20 (Playfield)
- `games/skateball.json#/lamps/18._note`: VLM lightmap: BL_L_l21 (Parts, Plastic1)
- `games/skateball.json#/lamps/19._note`: VLM lightmap: BL_L_l22 (LFlipperU, Parts, Playfield). Near lower left flipper.
- `games/skateball.json#/lamps/20._note`: VLM lightmap: BL_L_l23 (Playfield, RFlipper1U). Near upper right flipper.
- `games/skateball.json#/lamps/21._note`: VLM lightmap: BL_L_l24 (Parts, Playfield)
- `games/skateball.json#/lamps/22._note`: VLM lightmap: BL_L_L25 (Bumper2_Ring, Bumper2_Skirt, Parts, Spinner_sw33). Near middle bumper and spinner.
- `games/skateball.json#/lamps/23._note`: VLM lightmap: BL_L_l26 (Playfield)
- `games/skateball.json#/lamps/24._note`: VLM lightmap: BL_L_l28 (Parts, Plastics, Playfield, Star_sw30). Near left star rollover.
- `games/skateball.json#/lamps/25._note`: Backglass lamp. UpdateMultipleLamps: Controller.Lamp(29) drives FlBGL29 opacity. Comment: 'High Score To Date'.
- `games/skateball.json#/lamps/26._note`: VLM lightmap: BL_L_l30 (Parts, Playfield)
- `games/skateball.json#/lamps/27._note`: VLM lightmap: BL_L_l31 (Playfield)
- `games/skateball.json#/lamps/28._note`: VLM lightmap: BL_L_l33 (Playfield)
- `games/skateball.json#/lamps/29._note`: VLM lightmap: BL_L_l34 (Playfield)
- `games/skateball.json#/lamps/30._note`: VLM lightmap: BL_L_l35 (Playfield)
- `games/skateball.json#/lamps/31._note`: VLM lightmap: BL_L_l36 (Playfield)
- `games/skateball.json#/lamps/32._note`: VLM lightmap: BL_L_l37 (Parts)
- `games/skateball.json#/lamps/33._note`: VLM lightmap: BL_L_l38 (Parts, Playfield, RFlipperU). Near lower right flipper.
- `games/skateball.json#/lamps/34._note`: VLM lightmap: BL_L_l39 (Playfield)
- `games/skateball.json#/lamps/35._note`: VLM lightmap: BL_L_l40 (Parts, Playfield)
- `games/skateball.json#/lamps/36._note`: VLM lightmap: BL_L_L41 (Bumper2_Ring, Bumper3_Ring, Bumper3_Skirt, Parts, Plastics). Near middle and bottom bumpers.
- `games/skateball.json#/lamps/37._note`: VLM lightmap: BL_L_l42 (Playfield)
- `games/skateball.json#/lamps/38._note`: VLM lightmap: BL_L_l43 (Parts, Playfield). Also backglass lamp: UpdateMultipleLamps drives FlBGL43 opacity. Comment: 'Shoot Again'.
- `games/skateball.json#/lamps/39._note`: VLM lightmap: BL_L_l44 (Parts, Plastics, Playfield, Star_sw31). Near right star rollover.
- `games/skateball.json#/lamps/40._note`: Backglass lamp. UpdateMultipleLamps: Controller.Lamp(45) drives FlBGL27 (Game Over) and FlBGL45 (Match) opacity.
- `games/skateball.json#/lamps/41._note`: VLM lightmap: BL_L_l46 (Playfield)
- `games/skateball.json#/lamps/42._note`: VLM lightmap: BL_L_l47 (Parts, Playfield)
- `games/skateball.json#/lamps/43._note`: VLM lightmap: BL_L_l49 (Playfield)
- `games/skateball.json#/lamps/44._note`: VLM lightmap: BL_L_l50 (Playfield)
- `games/skateball.json#/lamps/45._note`: VLM lightmap: BL_L_l51 (Playfield)
- `games/skateball.json#/lamps/46._note`: VLM lightmap: BL_L_l52 (Playfield)
- `games/skateball.json#/lamps/47._note`: VLM lightmap: BL_L_l53 (Playfield)
- `games/skateball.json#/lamps/48._note`: VLM lightmap: BL_L_l54 (Parts, Playfield)
- `games/skateball.json#/lamps/49._note`: VLM lightmap: BL_L_l55 (Playfield)
- `games/skateball.json#/lamps/50._note`: VLM lightmap: BL_L_l56 (Parts, Playfield)
- `games/skateball.json#/lamps/51._note`: VLM lightmap: BL_L_L57 (Bumper1_Ring, DT_sw26, DT_sw27, Parts). Near top bumper and top drop targets.
- `games/skateball.json#/lamps/52._note`: VLM lightmap: BL_L_l58 (Parts, Playfield)
- `games/skateball.json#/lamps/53._note`: VLM lightmap: BL_L_l59 (Parts)
- `games/skateball.json#/lamps/54._note`: VLM lightmap: BL_L_l60 (Parts, Playfield, Spinner_sw33). Near spinner.
- `games/skateball.json#/lamps/55._note`: Backglass lamp. UpdateMultipleLamps: Controller.Lamp(61) drives FlBGL61 opacity. Comment: 'Tilt'.
- `games/skateball.json#/lamps/56._note`: VLM lightmap: BL_L_l62 (Parts, Playfield)
- `games/skateball.json#/lamps/57._note`: VLM lightmap: BL_L_l63 (Playfield)
- `games/skateball.json#/_source/confidence_notes`: High confidence extraction from VPW 1.0 release by mcarter78/apophis/VPW team. Platform identified as Bally -35 era from LoadVPM call: LoadVPM '03060000', 'Bally.vbs', 3.02. ROM name 'skatebll' from Const cGameName. No Const sw* definitions exist in script -- all switches identified from _Hit/_UnHit sub handlers, Controller.Switch() on/off calls, PulseSw calls, and DIP switch dialog context. Trough is a simple single-ball outhole design typical of 1980 Bally games: Drain_Hit sets Controller.Switch(8)=1, Drain_UnHit clears it, and SolBallRelease (solenoid 7) kicks ball from Drain kicker and clears switch 8. No cvpmTrough framework used -- this is a direct Controller.Switch ball management pattern. Saucer at sw5 uses Controller.Switch(5)=1 on hit, SolKicker (solenoid 2) kicks and clears switch 5. Three drop target banks: Left bank (sw20-24, 5 targets, reset by solenoid 8), Center bank (sw2-4, 3 targets, reset by solenoid 10), Top bank (sw26-28, 3 targets, reset by solenoid 9). All drop targets use DTHit/DTRaise Roth drop target system. Switch 32 is Right Flipper EOS/button switch -- manually set via Controller.Switch(32) in KeyDown/KeyUp for RightFlipperKey. Four flippers: LeftFlipper, RightFlipper, LeftFlipper1 (upper left), RightFlipper1 (upper right) using nFozzy flipper implementation with LF/RF/ULF/URF fire objects. Flipper solenoids from Bally.vbs framework constants: sLRFlipper=17, sLLFlipper=18, sULFlipper=20, sURFlipper=19. Solenoid 25 is GameOn relay (vpmNudge.SolGameOn). Solenoid 6 is knocker. Lamps identified from VLM (Visual Light Map) BL_L_ arrays -- 54 controlled lamps numbered l1 through l63 (not all sequential). Additional backglass lamps identified from UpdateMultipleLamps LampCallback: lamp 13 (Ball In Play), lamp 45 (Game Over), lamp 29 (High Score To Date), lamp 43 (Shoot Again), lamp 61 (Tilt). GI uses 31 light groups (GI001-GI031) driven by GiON/GiOFF subs, not ROM-controlled. No cvpmMech usage. Gates are purely decorative (6 gate animations, no switch triggers). Spinner at sw33. Three pop bumpers: Bumper1=sw40, Bumper2=sw38, Bumper3=sw39. Two slingshots: Left=sw37, Right=sw36.

## Unresolved questions

- Is the I/O enumeration complete for every supported physical/controller variant?
- Which inferred VPX behaviors reflect real hardware, and which are table-script conveniences?
- Are all mechanism home states, sensors, motion constraints, and ball interactions documented?

## Sources

- `legacy.game.skateball`: `games/skateball.json` at the pinned migration revision.
