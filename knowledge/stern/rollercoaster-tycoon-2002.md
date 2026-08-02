# RollerCoaster Tycoon

Coverage: **partial - source-derived recreation knowledge requiring validation**

## Overview

Legacy evidence identifies this candidate as Stern (2002). The information below is preserved for recreation work but is not automatically treated as validated physical-machine fact.

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

- `games/rct.json#/switches/0._note`: Custom trough — manual kick-chain from Drain through sw11-sw14
- `games/rct.json#/switches/3._note`: Ball eject position — SolRelease kicks from here
- `games/rct.json#/switches/4._note`: Pulsed briefly when SolRelease fires (sw14 kick), cleared on timer
- `games/rct.json#/switches/5._note`: Auto-plunger via cvpmImpulseP, plungerIM.switch 16
- `games/rct.json#/switches/6._note`: STHit 17
- `games/rct.json#/switches/7._note`: STHit 18
- `games/rct.json#/switches/8._note`: STHit 19
- `games/rct.json#/switches/9._note`: PulseSw 20 fired on each 30-degree disc rotation position. No VPX trigger — driven by SpinnerBallTimer code.
- `games/rct.json#/switches/11._note`: STHit 22
- `games/rct.json#/switches/17._note`: STHit 28
- `games/rct.json#/switches/18._note`: STHit 29
- `games/rct.json#/switches/19._note`: DTHit 30 — 3-bank drop targets (30/31/32)
- `games/rct.json#/switches/20._note`: DTHit 31
- `games/rct.json#/switches/21._note`: DTHit 32
- `games/rct.json#/switches/25._note`: Initialized closed. Opened by SolGhost (sol 19), closed by sw36_Hit when ball hits. Mechanically toggled target.
- `games/rct.json#/switches/26._note`: Starts disabled; enabled/disabled by sw37trigger/sw37trigger0 triggers
- `games/rct.json#/switches/27._note`: Initialized closed (Controller.Switch(38) = 1)
- `games/rct.json#/switches/28._note`: DTHit 39 — single drop target controlled by SolDTSweeperUp/Down (sols 4/5)
- `games/rct.json#/switches/29._note`: STHit 40
- `games/rct.json#/switches/31._note`: Kicker — ball locked until BallLock (sol 3) fires
- `games/rct.json#/switches/32._note`: STHit 44
- `games/rct.json#/switches/33._note`: STHit 45
- `games/rct.json#/switches/34._note`: STHit 46
- `games/rct.json#/switches/35._note`: Kicker — ball scooped until KioskScoop (sol 8) fires
- `games/rct.json#/switches/37._note`: PulseSw 49
- `games/rct.json#/switches/38._note`: PulseSw 50
- `games/rct.json#/switches/39._note`: PulseSw 51
- `games/rct.json#/switches/40._note`: Kicker — ball ejected when Rocket (sol 7) fires
- `games/rct.json#/switches/41._note`: vpmNudge.TiltSwitch = 56
- `games/rct.json#/switches/44._note`: PulseSw 59 — LeftSlingShot_Slingshot event
- `games/rct.json#/switches/47._note`: PulseSw 62 — RightSlingShot_Slingshot event
- `games/rct.json#/coils/0._vbscript_callback`: SolRelease
- `games/rct.json#/coils/0._inferred_type`: ball_management
- `games/rct.json#/coils/0._note`: Kicks from sw14 (trough eject position)
- `games/rct.json#/coils/1._vbscript_callback`: Auto_Plunger
- `games/rct.json#/coils/1._inferred_type`: auto_plunger
- `games/rct.json#/coils/2._vbscript_callback`: BallLock
- `games/rct.json#/coils/2._inferred_type`: kicker
- `games/rct.json#/coils/3._vbscript_callback`: SolDTSweeperUp
- `games/rct.json#/coils/3._inferred_type`: drop_target_reset
- `games/rct.json#/coils/3._note`: Single drop target sw39 — raises target and enables sweeper flipper
- `games/rct.json#/coils/4._vbscript_callback`: SolDTSweeperDown
- `games/rct.json#/coils/4._inferred_type`: drop_target
- `games/rct.json#/coils/4._note`: Single drop target sw39 — drops target and enables sweeper kick
- `games/rct.json#/coils/5._vbscript_callback`: SolDTDropDown
- `games/rct.json#/coils/5._inferred_type`: drop_target
- `games/rct.json#/coils/5._note`: Drops sw31 only
- `games/rct.json#/coils/6._vbscript_callback`: Rocket
- `games/rct.json#/coils/6._inferred_type`: kicker
- `games/rct.json#/coils/6._note`: Vertical up kick from rocket kicker
- `games/rct.json#/coils/7._vbscript_callback`: KioskScoop
- `games/rct.json#/coils/7._inferred_type`: kicker
- `games/rct.json#/coils/8._vbscript_callback`: SolDTDropUp
- `games/rct.json#/coils/8._inferred_type`: drop_target_reset
- `games/rct.json#/coils/8._note`: Resets 3-bank drop targets sw30/sw31/sw32
- `games/rct.json#/coils/9._vbscript_callback`: SolGhost
- `games/rct.json#/coils/9._inferred_type`: target_mechanism
- `games/rct.json#/coils/9._note`: Opens ghost target, sets sw36 closed
- `games/rct.json#/coils/10._vbscript_callback`: SolPost
- `games/rct.json#/coils/10._inferred_type`: up_post
- `games/rct.json#/coils/11._vbscript_callback`: FlashMod121
- `games/rct.json#/coils/11._inferred_type`: flasher
- `games/rct.json#/coils/11._note`: SolModCallback — PWM flasher
- `games/rct.json#/coils/12._vbscript_callback`: FlashMod122
- `games/rct.json#/coils/12._inferred_type`: flasher
- `games/rct.json#/coils/12._note`: SolModCallback — PWM flasher
- `games/rct.json#/coils/13._vbscript_callback`: FlashMod123
- `games/rct.json#/coils/13._inferred_type`: flasher
- `games/rct.json#/coils/13._note`: SolModCallback — PWM flasher
- `games/rct.json#/coils/14._vbscript_callback`: SolLock
- `games/rct.json#/coils/14._inferred_type`: diverter
- `games/rct.json#/coils/15._vbscript_callback`: SolDiverterRight
- `games/rct.json#/coils/15._inferred_type`: diverter
- `games/rct.json#/coils/16._vbscript_callback`: FlashMod127
- `games/rct.json#/coils/16._inferred_type`: flasher
- `games/rct.json#/coils/16._note`: SolModCallback — PWM flasher
- `games/rct.json#/coils/17._vbscript_callback`: DummyAnim
- `games/rct.json#/coils/17._inferred_type`: toy
- `games/rct.json#/coils/17._note`: Rotates DummyFlipper to end then back after 150ms
- `games/rct.json#/coils/18._vbscript_callback`: FlashMod129
- `games/rct.json#/coils/18._inferred_type`: flasher
- `games/rct.json#/coils/18._note`: SolModCallback — PWM flasher
- `games/rct.json#/coils/19._vbscript_callback`: FlashMod130
- `games/rct.json#/coils/19._inferred_type`: flasher
- `games/rct.json#/coils/19._note`: SolModCallback — PWM flasher
- `games/rct.json#/coils/20._vbscript_callback`: FlashMod131
- `games/rct.json#/coils/20._inferred_type`: flasher
- `games/rct.json#/coils/20._note`: SolModCallback — PWM flasher
- `games/rct.json#/coils/21._vbscript_callback`: FlashMod132
- `games/rct.json#/coils/21._inferred_type`: flasher
- `games/rct.json#/coils/21._note`: SolModCallback — PWM flasher
- `games/rct.json#/coils/22._vbscript_callback`: SolRFlipper
- `games/rct.json#/coils/22._inferred_type`: flipper
- `games/rct.json#/coils/22._note`: Framework constant sLRFlipper from sega.vbs
- `games/rct.json#/coils/23._vbscript_callback`: SolLFlipper
- `games/rct.json#/coils/23._inferred_type`: flipper
- `games/rct.json#/coils/23._note`: Framework constant sLLFlipper from sega.vbs
- `games/rct.json#/coils/24._vbscript_callback`: SolURFlipper
- `games/rct.json#/coils/24._inferred_type`: flipper
- `games/rct.json#/coils/24._note`: Framework constant sURFlipper from sega.vbs
- `games/rct.json#/coils/25._vbscript_callback`: SolULFlipper
- `games/rct.json#/coils/25._inferred_type`: flipper
- `games/rct.json#/coils/25._note`: Framework constant sULFlipper from sega.vbs
- `games/rct.json#/lamps/0._note`: vpmMapLights insert lamp
- `games/rct.json#/lamps/1._note`: vpmMapLights insert lamp
- `games/rct.json#/lamps/2._note`: vpmMapLights insert lamp
- `games/rct.json#/lamps/3._note`: vpmMapLights insert lamp
- `games/rct.json#/lamps/4._note`: vpmMapLights insert lamp
- `games/rct.json#/lamps/5._note`: vpmMapLights insert lamp
- `games/rct.json#/lamps/6._note`: vpmMapLights insert lamp
- `games/rct.json#/lamps/7._note`: vpmMapLights insert lamp
- `games/rct.json#/lamps/8._note`: vpmMapLights insert lamp
- `games/rct.json#/lamps/9._note`: vpmMapLights insert lamp
- `games/rct.json#/lamps/10._note`: vpmMapLights insert lamp
- `games/rct.json#/lamps/11._note`: vpmMapLights insert lamp
- `games/rct.json#/lamps/12._note`: vpmMapLights insert lamp
- `games/rct.json#/lamps/13._note`: vpmMapLights insert lamp
- `games/rct.json#/lamps/14._note`: vpmMapLights insert lamp
- `games/rct.json#/lamps/15._note`: vpmMapLights insert lamp
- `games/rct.json#/lamps/16._note`: vpmMapLights insert lamp
- `games/rct.json#/lamps/17._note`: vpmMapLights insert lamp
- `games/rct.json#/lamps/18._note`: vpmMapLights insert lamp
- `games/rct.json#/lamps/19._note`: vpmMapLights insert lamp
- `games/rct.json#/lamps/20._note`: vpmMapLights insert lamp
- `games/rct.json#/lamps/21._note`: vpmMapLights insert lamp
- `games/rct.json#/lamps/22._note`: vpmMapLights insert lamp
- `games/rct.json#/lamps/23._note`: vpmMapLights insert lamp
- `games/rct.json#/lamps/24._note`: vpmMapLights insert lamp
- `games/rct.json#/lamps/25._note`: vpmMapLights insert lamp
- `games/rct.json#/lamps/26._note`: vpmMapLights insert lamp
- `games/rct.json#/lamps/27._note`: vpmMapLights insert lamp
- `games/rct.json#/lamps/28._note`: vpmMapLights insert lamp
- `games/rct.json#/lamps/29._note`: vpmMapLights insert lamp
- `games/rct.json#/lamps/30._note`: vpmMapLights insert lamp
- `games/rct.json#/lamps/31._note`: vpmMapLights insert lamp
- `games/rct.json#/lamps/32._note`: vpmMapLights insert lamp
- `games/rct.json#/lamps/33._note`: vpmMapLights insert lamp
- `games/rct.json#/lamps/34._note`: vpmMapLights insert lamp
- `games/rct.json#/lamps/35._note`: vpmMapLights insert lamp
- `games/rct.json#/lamps/36._note`: vpmMapLights insert lamp
- `games/rct.json#/lamps/37._note`: vpmMapLights insert lamp
- `games/rct.json#/lamps/38._note`: vpmMapLights insert lamp
- `games/rct.json#/lamps/39._note`: vpmMapLights insert lamp
- `games/rct.json#/lamps/40._note`: vpmMapLights insert lamp
- `games/rct.json#/lamps/41._note`: vpmMapLights insert lamp
- `games/rct.json#/lamps/42._note`: vpmMapLights insert lamp
- `games/rct.json#/lamps/43._note`: vpmMapLights insert lamp
- `games/rct.json#/lamps/44._note`: vpmMapLights insert lamp
- `games/rct.json#/lamps/45._note`: vpmMapLights insert lamp
- `games/rct.json#/lamps/46._note`: vpmMapLights insert lamp
- `games/rct.json#/lamps/47._note`: vpmMapLights insert lamp — VLM-classified as Flashers but controlled as lamp
- `games/rct.json#/lamps/48._note`: vpmMapLights insert lamp
- `games/rct.json#/lamps/49._note`: vpmMapLights insert lamp
- `games/rct.json#/lamps/50._note`: vpmMapLights insert lamp
- `games/rct.json#/lamps/51._note`: vpmMapLights insert lamp
- `games/rct.json#/lamps/52._note`: vpmMapLights insert lamp
- `games/rct.json#/lamps/53._note`: vpmMapLights insert lamp
- `games/rct.json#/lamps/54._note`: vpmMapLights insert lamp
- `games/rct.json#/lamps/55._note`: vpmMapLights insert lamp
- `games/rct.json#/lamps/56._note`: vpmMapLights insert lamp — VLM-classified as Flashers; also drives Bumper2 force variation via L57_animate
- `games/rct.json#/lamps/57._note`: vpmMapLights insert lamp — VLM-classified as Flashers; also drives Bumper3 force variation via L58_animate
- `games/rct.json#/lamps/58._note`: vpmMapLights insert lamp — VLM-classified as Flashers; also drives Bumper1 force variation via L59_animate
- `games/rct.json#/lamps/59._note`: vpmMapLights insert lamp
- `games/rct.json#/lamps/60._note`: vpmMapLights insert lamp
- `games/rct.json#/lamps/61._note`: vpmMapLights insert lamp
- `games/rct.json#/lamps/62._note`: vpmMapLights insert lamp
- `games/rct.json#/lamps/63._note`: Start button lamp — L64_animate controls startbutton.BlendDisableLighting
- `games/rct.json#/lamps/64._note`: vpmMapLights backlight lamp
- `games/rct.json#/lamps/65._note`: vpmMapLights backlight lamp
- `games/rct.json#/lamps/66._note`: vpmMapLights backlight lamp
- `games/rct.json#/lamps/67._note`: vpmMapLights backlight lamp
- `games/rct.json#/lamps/68._note`: vpmMapLights backlight lamp
- `games/rct.json#/lamps/69._note`: vpmMapLights insert lamp
- `games/rct.json#/lamps/70._note`: vpmMapLights insert lamp
- `games/rct.json#/lamps/71._note`: vpmMapLights insert lamp
- `games/rct.json#/lamps/72._note`: vpmMapLights backlight lamp
- `games/rct.json#/lamps/73._note`: vpmMapLights backlight lamp
- `games/rct.json#/lamps/74._note`: vpmMapLights backlight lamp
- `games/rct.json#/lamps/75._note`: vpmMapLights backlight lamp
- `games/rct.json#/lamps/76._note`: vpmMapLights backlight lamp
- `games/rct.json#/lamps/77._note`: vpmMapLights insert lamp
- `games/rct.json#/lamps/78._note`: vpmMapLights insert lamp
- `games/rct.json#/_source/confidence_notes`: High confidence on switches/coils from Controller.Switch() calls and SolCallback assignments. SEGA/Whitestar platform detected from LoadVPM sega.vbs. Trough is custom (no cvpmTrough/cvpmBallStack) — 4 ball positions sw11-sw14 with manual kick-chain logic. Lamps inferred from VLM naming (LM_Inserts_L*, LM_Backlight_L*) since vpmMapLights is used with InsertLamps collection; exact lamp descriptions unavailable from VBS alone. Flasher coils (21-23, 27, 29-32) use SolModCallback for PWM. Switch 20 is the Scrambled Eggs disc spinner (pulsed on rotation). Switch 36 is a ghost target (mechanically toggled by sol 19). L48/L57/L58/L59 are VLM-classified as flashers but mapped as regular lamps (<80). L64 (start button) has an animate sub but no VLM reference. Flipper coil IDs from sega.vbs constants.

## Unresolved questions

- Is the I/O enumeration complete for every supported physical/controller variant?
- Which inferred VPX behaviors reflect real hardware, and which are table-script conveniences?
- Are all mechanism home states, sensors, motion constraints, and ball interactions documented?

## Sources

- `legacy.game.rct`: `games/rct.json` at the pinned migration revision.
