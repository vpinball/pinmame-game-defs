# Bad Cats

Coverage: **partial - source-derived recreation knowledge requiring validation**

## Overview

Legacy evidence identifies this candidate as Williams (1989). The information below is preserved for recreation work but is not automatically treated as validated physical-machine fact.

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

- `games/bcats.json#/switches/0._vbscript_name`: swTilt
- `games/bcats.json#/switches/0._note`: Framework-defined (S11.vbs). Used as vpmNudge.TiltSwitch.
- `games/bcats.json#/switches/1._vbscript_name`: swBallRollTilt
- `games/bcats.json#/switches/1._note`: Framework-defined (S11.vbs)
- `games/bcats.json#/switches/2._vbscript_name`: swStartButton
- `games/bcats.json#/switches/2._note`: Framework-defined (S11.vbs)
- `games/bcats.json#/switches/3._vbscript_name`: swCoin3
- `games/bcats.json#/switches/3._note`: Framework-defined (S11.vbs)
- `games/bcats.json#/switches/4._vbscript_name`: swCoin2
- `games/bcats.json#/switches/4._note`: Framework-defined (S11.vbs)
- `games/bcats.json#/switches/5._vbscript_name`: swCoin1
- `games/bcats.json#/switches/5._note`: Framework-defined (S11.vbs)
- `games/bcats.json#/switches/6._vbscript_name`: swSlamTilt
- `games/bcats.json#/switches/6._note`: Framework-defined (S11.vbs)
- `games/bcats.json#/switches/7._vbscript_name`: swHiScoreReset
- `games/bcats.json#/switches/7._note`: Framework-defined (S11.vbs)
- `games/bcats.json#/switches/8._vbscript_name`: sw10
- `games/bcats.json#/switches/8._note`: Single-ball trough. Ball created here at init. Controller.Switch(10)=1 at startup.
- `games/bcats.json#/switches/9._vbscript_name`: sw11
- `games/bcats.json#/switches/9._note`: Upper playfield standup target, near rollover lanes. Has animation primitive.
- `games/bcats.json#/switches/10._vbscript_name`: sw12
- `games/bcats.json#/switches/10._note`: Upper playfield standup target. Has animation primitive.
- `games/bcats.json#/switches/11._vbscript_name`: sw13
- `games/bcats.json#/switches/11._note`: Upper playfield standup target. Has animation primitive.
- `games/bcats.json#/switches/12._vbscript_name`: sw14
- `games/bcats.json#/switches/12._note`: Upper playfield standup target. Has animation primitive.
- `games/bcats.json#/switches/13._vbscript_name`: sw16
- `games/bcats.json#/switches/13._note`: Fishbowl ramp gate switch. PulseSw. Has gate wire animation primitive.
- `games/bcats.json#/switches/14._vbscript_name`: LT19
- `games/bcats.json#/switches/14._note`: Linear target (Fish Bone-Us). Uses LinearTarget class with custom hit detection. Switch activated via controller.Switch(19).
- `games/bcats.json#/switches/15._vbscript_name`: sw22
- `games/bcats.json#/switches/15._note`: Doghouse scoop eject hole. Ball enters and is kicked out by SolDogOut (solenoid 3).
- `games/bcats.json#/switches/16._vbscript_name`: sw23
- `games/bcats.json#/switches/16._note`: Tiger ramp gate switch. PulseSw. Has gate wire animation primitive.
- `games/bcats.json#/switches/17._vbscript_name`: sw24
- `games/bcats.json#/switches/17._note`: Trash can / Garbage can eject hole (Fish Bone-Us collection). Ball kicked out by SolTrashOut (solenoid 5).
- `games/bcats.json#/switches/18._vbscript_name`: sw25
- `games/bcats.json#/switches/18._note`: Bird drop target bank, target 1. DTHit handler. Reset by solenoid 6 (SolBT).
- `games/bcats.json#/switches/19._vbscript_name`: sw26
- `games/bcats.json#/switches/19._note`: Bird drop target bank, target 2. DTHit handler.
- `games/bcats.json#/switches/20._vbscript_name`: sw27
- `games/bcats.json#/switches/20._note`: Bird drop target bank, target 3. DTHit handler.
- `games/bcats.json#/switches/21._vbscript_name`: sw28
- `games/bcats.json#/switches/21._note`: Bird drop target bank, target 4. DTHit handler.
- `games/bcats.json#/switches/22._vbscript_name`: sw29
- `games/bcats.json#/switches/22._note`: Bird drop target bank, target 5. DTHit handler.
- `games/bcats.json#/switches/23._vbscript_name`: sw30
- `games/bcats.json#/switches/23._note`: Left inlane rollover. Lights Doghouse when lit.
- `games/bcats.json#/switches/24._vbscript_name`: sw31
- `games/bcats.json#/switches/24._note`: Right inlane rollover. Lights 10x Fish Bone-Us multiplier when lit.
- `games/bcats.json#/switches/25._vbscript_name`: sw33
- `games/bcats.json#/switches/25._note`: TOY rollover lane, letter T. PulseSw.
- `games/bcats.json#/switches/26._vbscript_name`: sw34
- `games/bcats.json#/switches/26._note`: TOY rollover lane, letter O. PulseSw.
- `games/bcats.json#/switches/27._vbscript_name`: sw35
- `games/bcats.json#/switches/27._note`: Left outlane. Triggers backglass animation and Curiosity Spin on final ball.
- `games/bcats.json#/switches/28._vbscript_name`: sw36
- `games/bcats.json#/switches/28._note`: Right outlane.
- `games/bcats.json#/switches/29._vbscript_name`: sw37
- `games/bcats.json#/switches/29._note`: Milk bottle drop target bank, target 1. DTHit handler. Reset by solenoid 4 (solMT).
- `games/bcats.json#/switches/30._vbscript_name`: sw38
- `games/bcats.json#/switches/30._note`: Milk bottle drop target bank, target 2. DTHit handler.
- `games/bcats.json#/switches/31._vbscript_name`: sw39
- `games/bcats.json#/switches/31._note`: Milk bottle drop target bank, target 3. DTHit handler.
- `games/bcats.json#/switches/32._vbscript_name`: sw40
- `games/bcats.json#/switches/32._note`: TOY rollover lane, letter Y. PulseSw.
- `games/bcats.json#/switches/33._vbscript_name`: sw41
- `games/bcats.json#/switches/33._note`: Spinner switch. Has rotating animation primitive (sw41P). SoundSpinner plays spinner sound at sw41 position.
- `games/bcats.json#/switches/34._vbscript_name`: sw43
- `games/bcats.json#/switches/34._note`: Right side gate/trigger. Has rotating animation primitive (sw43P) with timer-driven animation.
- `games/bcats.json#/switches/35._note`: Defined in cvpmMech mechanism, not as a direct VPX switch. Mech .AddSw 44, 0, 99. Seafood wheel position detection.
- `games/bcats.json#/switches/36._vbscript_name`: sw60
- `games/bcats.json#/switches/36._note`: Upper jet bumper. PulseSw. Has ring animation.
- `games/bcats.json#/switches/37._vbscript_name`: sw61
- `games/bcats.json#/switches/37._note`: Left jet bumper. PulseSw. Has ring animation.
- `games/bcats.json#/switches/38._vbscript_name`: sw62
- `games/bcats.json#/switches/38._note`: Lower jet bumper. PulseSw. Has ring animation.
- `games/bcats.json#/switches/39._note`: Left slingshot. PulseSw(63) in LeftSlingShot_Slingshot sub. Part of vpmNudge.TiltObj array.
- `games/bcats.json#/switches/40._note`: Right slingshot. PulseSw(64) in RightSlingShot_Slingshot sub. Part of vpmNudge.TiltObj array.
- `games/bcats.json#/switches/41._vbscript_name`: swURFlip
- `games/bcats.json#/switches/41._note`: Framework-defined (S11.vbs). Cabinet flipper button switch.
- `games/bcats.json#/switches/42._vbscript_name`: swLRFlip
- `games/bcats.json#/switches/42._note`: Framework-defined (S11.vbs). Cabinet flipper button switch.
- `games/bcats.json#/switches/43._vbscript_name`: swULFlip
- `games/bcats.json#/switches/43._note`: Framework-defined (S11.vbs). Cabinet flipper button switch.
- `games/bcats.json#/switches/44._vbscript_name`: swLLFlip
- `games/bcats.json#/switches/44._note`: Framework-defined (S11.vbs). Cabinet flipper button switch.
- `games/bcats.json#/coils/0._vbscript_callback`: SolBallRelease
- `games/bcats.json#/coils/0._inferred_type`: ball_management
- `games/bcats.json#/coils/0._note`: Kicks ball from outhole (sw10) to shooter lane. BIP incremented on fire.
- `games/bcats.json#/coils/1._vbscript_callback`: KnockerSolenoid
- `games/bcats.json#/coils/1._inferred_type`: knocker
- `games/bcats.json#/coils/2._vbscript_callback`: SolDogOut
- `games/bcats.json#/coils/2._inferred_type`: kicker
- `games/bcats.json#/coils/2._note`: Ejects ball from doghouse scoop (sw22). Kicks at angle 35, power 35.
- `games/bcats.json#/coils/3._vbscript_callback`: solMT
- `games/bcats.json#/coils/3._inferred_type`: drop_target_reset
- `games/bcats.json#/coils/3._note`: Resets milk bottle drop targets (sw37, sw38, sw39). Original comment: dtMilk.SolDropUp
- `games/bcats.json#/coils/4._vbscript_callback`: SolTrashOut
- `games/bcats.json#/coils/4._inferred_type`: kicker
- `games/bcats.json#/coils/4._note`: Ejects ball from trash can/garbage can kicker (sw24).
- `games/bcats.json#/coils/5._vbscript_callback`: SolBT
- `games/bcats.json#/coils/5._inferred_type`: drop_target_reset
- `games/bcats.json#/coils/5._note`: Resets bird drop targets (sw25-sw29). Original comment: dtBird.SolDropUp
- `games/bcats.json#/coils/6._vbscript_callback`: SolbgCat
- `games/bcats.json#/coils/6._inferred_type`: backglass_mechanism
- `games/bcats.json#/coils/6._note`: Triggers backglass cat animation (VR: vrCatTimer). Mechanical backbox feature.
- `games/bcats.json#/coils/7._vbscript_callback`: SolGIBlink
- `games/bcats.json#/coils/7._inferred_type`: gi_relay
- `games/bcats.json#/coils/7._note`: Blinks GI on/off. Toggles both main GI (SolGI) and backbox GI (SolbbGI) when their respective active flags are set.
- `games/bcats.json#/coils/8._vbscript_callback`: SolbbGION
- `games/bcats.json#/coils/8._inferred_type`: gi_relay
- `games/bcats.json#/coils/8._note`: Controls backbox GI string. Sets GIActivebb flag.
- `games/bcats.json#/coils/9._vbscript_callback`: SolbgWoman
- `games/bcats.json#/coils/9._inferred_type`: backglass_mechanism
- `games/bcats.json#/coils/9._note`: Triggers backglass woman-with-broom animation (VR: vrWomanTimer and VrCat rotation). Mechanical backbox feature.
- `games/bcats.json#/coils/10._vbscript_callback`: FlashMod15
- `games/bcats.json#/coils/10._inferred_type`: flasher
- `games/bcats.json#/coils/10._note`: Seafood wheel light/flasher. Also used as cvpmMech Sol1 for wheel motor direction. SolModCallback (PWM).
- `games/bcats.json#/coils/11._inferred_type`: mechanism
- `games/bcats.json#/coils/11._note`: cvpmMech Sol2 for seafood wheel. No SolCallback assigned directly. SolModCallback(16) commented out with note: secondary seafood flasher solenoid - apparently doesn't exist IRL.
- `games/bcats.json#/coils/12._vbscript_callback`: SolGION
- `games/bcats.json#/coils/12._inferred_type`: gi_relay
- `games/bcats.json#/coils/12._note`: GameOnSolenoid (framework-defined = 23). Controls main playfield GI. Also enables flippers. Sets GIActive flag. Also calls ACRelay via vpmNudge.SolGameOn.
- `games/bcats.json#/coils/13._vbscript_callback`: FlashMod125
- `games/bcats.json#/coils/13._inferred_type`: flasher
- `games/bcats.json#/coils/13._note`: SolModCallback (PWM). Controller.SolMask(1025). Fish target area flasher.
- `games/bcats.json#/coils/14._vbscript_callback`: FlashMod126
- `games/bcats.json#/coils/14._inferred_type`: flasher
- `games/bcats.json#/coils/14._note`: SolModCallback (PWM). Controller.SolMask(1026). Has mayo/grease glass effect.
- `games/bcats.json#/coils/15._vbscript_callback`: FlashMod127
- `games/bcats.json#/coils/15._inferred_type`: flasher
- `games/bcats.json#/coils/15._note`: SolModCallback (PWM). Controller.SolMask(1027). Has mayo/grease glass effect.
- `games/bcats.json#/coils/16._vbscript_callback`: FlashMod128
- `games/bcats.json#/coils/16._inferred_type`: flasher
- `games/bcats.json#/coils/16._note`: SolModCallback (PWM). Controller.SolMask(1028). Has mayo/grease glass effect.
- `games/bcats.json#/coils/17._vbscript_callback`: FlashMod129
- `games/bcats.json#/coils/17._inferred_type`: flasher
- `games/bcats.json#/coils/17._note`: SolModCallback (PWM). Controller.SolMask(1029). Has mayo/grease glass effect.
- `games/bcats.json#/coils/18._vbscript_callback`: FlashMod130
- `games/bcats.json#/coils/18._inferred_type`: flasher
- `games/bcats.json#/coils/18._note`: SolModCallback (PWM). Controller.SolMask(1030).
- `games/bcats.json#/coils/19._vbscript_callback`: FlashMod131
- `games/bcats.json#/coils/19._inferred_type`: flasher
- `games/bcats.json#/coils/19._note`: SolModCallback (PWM). Controller.SolMask(1031). Has mayo/grease glass effect.
- `games/bcats.json#/coils/20._vbscript_callback`: FlashMod132
- `games/bcats.json#/coils/20._inferred_type`: flasher
- `games/bcats.json#/coils/20._note`: SolModCallback (PWM). Controller.SolMask(1032). BBQ/barbecue area flasher.
- `games/bcats.json#/coils/21._vbscript_name`: sLRFlipper
- `games/bcats.json#/coils/21._vbscript_callback`: SolRFlipper
- `games/bcats.json#/coils/21._inferred_type`: flipper
- `games/bcats.json#/coils/21._note`: Framework-defined constant (core.vbs: sLRFlipper=46)
- `games/bcats.json#/coils/22._vbscript_name`: sLLFlipper
- `games/bcats.json#/coils/22._vbscript_callback`: SolLFlipper
- `games/bcats.json#/coils/22._inferred_type`: flipper
- `games/bcats.json#/coils/22._note`: Framework-defined constant (core.vbs: sLLFlipper=48)
- `games/bcats.json#/lamps/0._vlm_array`: BL_Inserts_l1
- `games/bcats.json#/lamps/0._note`: Near left/right flipper area based on VLM lightmap data (FlipperL, FlipperR)
- `games/bcats.json#/lamps/1._vlm_array`: BL_Inserts_l2
- `games/bcats.json#/lamps/1._note`: Left slingshot area based on VLM lightmap data
- `games/bcats.json#/lamps/2._vlm_array`: BL_Inserts_l3
- `games/bcats.json#/lamps/2._note`: Playfield insert
- `games/bcats.json#/lamps/3._vlm_array`: BL_Inserts_l4
- `games/bcats.json#/lamps/3._note`: Playfield insert
- `games/bcats.json#/lamps/4._vlm_array`: BL_Inserts_l5
- `games/bcats.json#/lamps/4._note`: Right flipper area based on VLM lightmap data
- `games/bcats.json#/lamps/5._vlm_array`: BL_Inserts_l6
- `games/bcats.json#/lamps/5._note`: Playfield insert
- `games/bcats.json#/lamps/6._vlm_array`: BL_Inserts_l7
- `games/bcats.json#/lamps/6._note`: Right slingshot area based on VLM lightmap data
- `games/bcats.json#/lamps/7._vlm_array`: BL_Inserts_l8
- `games/bcats.json#/lamps/7._note`: Playfield insert near plastics
- `games/bcats.json#/lamps/8._vlm_array`: BL_Inserts_l9
- `games/bcats.json#/lamps/8._note`: Upper playfield area based on VLM lightmap data (BackWall2)
- `games/bcats.json#/lamps/9._vlm_array`: BL_Inserts_l10
- `games/bcats.json#/lamps/9._note`: Tiger ramp area based on VLM lightmap data
- `games/bcats.json#/lamps/10._vlm_array`: BL_Inserts_l11
- `games/bcats.json#/lamps/10._note`: Upper playfield area
- `games/bcats.json#/lamps/11._vlm_array`: BL_Inserts_l12
- `games/bcats.json#/lamps/11._note`: Upper playfield area
- `games/bcats.json#/lamps/12._vlm_array`: BL_Inserts_l13
- `games/bcats.json#/lamps/12._note`: Upper playfield area
- `games/bcats.json#/lamps/13._vlm_array`: BL_Inserts_l14
- `games/bcats.json#/lamps/13._note`: Near upper bumper (sw60) area based on VLM lightmap data
- `games/bcats.json#/lamps/14._vlm_array`: BL_Inserts_l15
- `games/bcats.json#/lamps/14._note`: Near upper bumper (sw60) area based on VLM lightmap data
- `games/bcats.json#/lamps/15._vlm_array`: BL_Inserts_l16
- `games/bcats.json#/lamps/15._note`: Near bumper area (sw60/sw61) based on VLM lightmap data
- `games/bcats.json#/lamps/16._vlm_array`: BL_Inserts_l17
- `games/bcats.json#/lamps/16._note`: Tiger ramp area based on VLM lightmap data
- `games/bcats.json#/lamps/17._vlm_array`: BL_Inserts_l18
- `games/bcats.json#/lamps/17._note`: Upper playfield area
- `games/bcats.json#/lamps/18._vlm_array`: BL_Inserts_l19
- `games/bcats.json#/lamps/18._note`: Tiger ramp area based on VLM lightmap data
- `games/bcats.json#/lamps/19._vlm_array`: BL_Inserts_l21
- `games/bcats.json#/lamps/19._note`: Fish ramp area based on VLM lightmap data (FishRampEdges)
- `games/bcats.json#/lamps/20._vlm_array`: BL_Inserts_l22
- `games/bcats.json#/lamps/20._note`: Fish ramp area based on VLM lightmap data
- `games/bcats.json#/lamps/21._vlm_array`: BL_Inserts_l23
- `games/bcats.json#/lamps/21._note`: Fish ramp area based on VLM lightmap data
- `games/bcats.json#/lamps/22._vlm_array`: BL_Inserts_l24
- `games/bcats.json#/lamps/22._note`: Near fish ramp gate (sw16) based on VLM lightmap data
- `games/bcats.json#/lamps/23._vlm_array`: BL_Inserts_l26
- `games/bcats.json#/lamps/23._note`: Left slingshot area based on VLM lightmap data
- `games/bcats.json#/lamps/24._vlm_array`: BL_Inserts_l27
- `games/bcats.json#/lamps/24._note`: Playfield insert
- `games/bcats.json#/lamps/25._vlm_array`: BL_Inserts_l28
- `games/bcats.json#/lamps/25._note`: Tiger ramp edge area based on VLM lightmap data
- `games/bcats.json#/lamps/26._vlm_array`: BL_Inserts_l29
- `games/bcats.json#/lamps/26._note`: Right slingshot area based on VLM lightmap data
- `games/bcats.json#/lamps/27._vlm_array`: BL_Inserts_l30
- `games/bcats.json#/lamps/27._note`: Playfield insert
- `games/bcats.json#/lamps/28._vlm_array`: BL_Inserts_l33
- `games/bcats.json#/lamps/28._note`: Playfield insert
- `games/bcats.json#/lamps/29._vlm_array`: BL_Inserts_l34
- `games/bcats.json#/lamps/29._note`: Playfield insert
- `games/bcats.json#/lamps/30._vlm_array`: BL_Inserts_l35
- `games/bcats.json#/lamps/30._note`: Playfield insert
- `games/bcats.json#/lamps/31._vlm_array`: BL_Inserts_l36
- `games/bcats.json#/lamps/31._note`: Playfield insert
- `games/bcats.json#/lamps/32._vlm_array`: BL_Inserts_l37
- `games/bcats.json#/lamps/32._note`: Playfield insert
- `games/bcats.json#/lamps/33._vlm_array`: BL_Inserts_l38
- `games/bcats.json#/lamps/33._note`: Playfield insert
- `games/bcats.json#/lamps/34._vlm_array`: BL_Inserts_l39
- `games/bcats.json#/lamps/34._note`: Playfield insert
- `games/bcats.json#/lamps/35._vlm_array`: BL_Inserts_l40
- `games/bcats.json#/lamps/35._note`: Playfield insert near plastics
- `games/bcats.json#/lamps/36._vlm_array`: BL_Inserts_l41
- `games/bcats.json#/lamps/36._note`: Playfield insert
- `games/bcats.json#/lamps/37._vlm_array`: BL_Inserts_l42
- `games/bcats.json#/lamps/37._note`: Playfield insert
- `games/bcats.json#/lamps/38._vlm_array`: BL_Inserts_l43
- `games/bcats.json#/lamps/38._note`: Playfield insert
- `games/bcats.json#/lamps/39._vlm_array`: BL_Inserts_l44
- `games/bcats.json#/lamps/39._note`: Playfield insert
- `games/bcats.json#/lamps/40._vlm_array`: BL_Inserts_l45
- `games/bcats.json#/lamps/40._note`: Playfield insert
- `games/bcats.json#/lamps/41._vlm_array`: BL_Inserts_l46
- `games/bcats.json#/lamps/41._note`: Under-playfield lamp only
- `games/bcats.json#/lamps/42._vlm_array`: BL_Inserts_l47
- `games/bcats.json#/lamps/42._note`: Backglass area based on VLM lightmap data
- `games/bcats.json#/lamps/43._vlm_array`: BL_Inserts_l48
- `games/bcats.json#/lamps/43._note`: Backglass area based on VLM lightmap data
- `games/bcats.json#/lamps/44._vlm_array`: BL_Inserts_l49
- `games/bcats.json#/lamps/44._note`: Playfield insert
- `games/bcats.json#/lamps/45._vlm_array`: BL_Inserts_l50
- `games/bcats.json#/lamps/45._note`: Playfield insert
- `games/bcats.json#/lamps/46._vlm_array`: BL_Inserts_l51
- `games/bcats.json#/lamps/46._note`: Playfield insert
- `games/bcats.json#/lamps/47._vlm_array`: BL_Inserts_l52
- `games/bcats.json#/lamps/47._note`: Playfield insert
- `games/bcats.json#/lamps/48._vlm_array`: BL_Inserts_l53
- `games/bcats.json#/lamps/48._note`: Near fish target based on VLM lightmap data (FishT)
- `games/bcats.json#/_source/confidence_notes`: High confidence on switches/coils. Lamp descriptions inferred from VLM insert arrays (BL_Inserts_lN) and playfield context; no named lamp constants in script. Uses S11.VBS framework (System 11B). Cabinet switches (1-8, 81-84) from S11.vbs framework constants. Flipper solenoids (46/48) from core.vbs framework constants. Seafood wheel mechanism uses cvpmMech with Sol1=16, Sol2=15 and switch 44. SolModCallback used for flashers (PWM). SolCallback(16) commented out as secondary seafood flasher solenoid that apparently doesn't exist IRL.

## Unresolved questions

- Is the I/O enumeration complete for every supported physical/controller variant?
- Which inferred VPX behaviors reflect real hardware, and which are table-script conveniences?
- Are all mechanism home states, sensors, motion constraints, and ball interactions documented?

## Sources

- `legacy.game.bcats`: `games/bcats.json` at the pinned migration revision.
