# Austin Powers

Coverage: **partial - source-derived recreation knowledge requiring validation**

## Overview

Legacy evidence identifies this candidate as Stern (2001). The information below is preserved for recreation work but is not automatically treated as validated physical-machine fact.

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

- `games/austin.json#/switches/0._note`: cvpmTrough InitSwitches Array(14,13,12,11) — sw11 is nearest shooter
- `games/austin.json#/switches/4._note`: PulseSw 15 fired in SolTrough after ball eject. Confirms ball reached shooter lane.
- `games/austin.json#/switches/5._note`: Controller.Switch on/off (rollover). Also plungerIM.switch 16 — auto plunger lane switch.
- `games/austin.json#/switches/6._note`: PulseSw 18
- `games/austin.json#/switches/7._note`: bsInodoro cvpmSaucer. InitKicker Sw21, 21. Ball management.
- `games/austin.json#/switches/8._note`: mEvil.AddSw 22, 498, 500. Mechanism switch — Dr Evil at top position.
- `games/austin.json#/switches/9._note`: mEvil.AddSw 23, 0, 1. Mechanism switch — Dr Evil at bottom/home position.
- `games/austin.json#/switches/10._note`: PulseSw 24. Animated standup target near Dr Evil.
- `games/austin.json#/switches/11._note`: PulseSw 25
- `games/austin.json#/switches/12._note`: PulseSw 26
- `games/austin.json#/switches/13._note`: PulseSw 27
- `games/austin.json#/switches/14._note`: PulseSw 28
- `games/austin.json#/switches/15._note`: PulseSw 29
- `games/austin.json#/switches/16._note`: PulseSw 30
- `games/austin.json#/switches/17._note`: PulseSw 31. Animated standup target.
- `games/austin.json#/switches/18._note`: PulseSw 32. Animated standup target.
- `games/austin.json#/switches/19._note`: Controller.Switch on/off
- `games/austin.json#/switches/20._note`: PulseSw 34 from spinner animation timer. Animated Mini-Me spinner.
- `games/austin.json#/switches/21._note`: PulseSw 35
- `games/austin.json#/switches/22._note`: PulseSw 37 on hit and unhit
- `games/austin.json#/switches/23._note`: PulseSw 38 on hit and unhit
- `games/austin.json#/switches/24._note`: Controller.Switch on/off
- `games/austin.json#/switches/25._note`: PulseSw 41 on hit and unhit
- `games/austin.json#/switches/26._note`: PulseSw 42 on hit and unhit
- `games/austin.json#/switches/27._note`: mLaserGun.AddSw 43, 0, 10. Mechanism switch — cannon at home position.
- `games/austin.json#/switches/28._note`: mLaserGun.AddSw 44, 400, 750. Mechanism switch — cannon at end of travel.
- `games/austin.json#/switches/29._note`: Controller.switch(45) on/off. Ball enters cannon, kicked out by SolLaserBeam (coil 4).
- `games/austin.json#/switches/30._note`: bsScoop cvpmSaucer. InitKicker Sw46b, 46.
- `games/austin.json#/switches/31._note`: Controller.Switch on/off
- `games/austin.json#/switches/32._note`: Controller.Switch on/off
- `games/austin.json#/switches/33._note`: PulseSw 49
- `games/austin.json#/switches/34._note`: PulseSw 50
- `games/austin.json#/switches/35._note`: PulseSw 51
- `games/austin.json#/switches/36._note`: Controller.Switch(53) set via LeftMagnaSave/RightMagnaSave/LockBarKey
- `games/austin.json#/switches/37._note`: vpmNudge.TiltSwitch = 56
- `games/austin.json#/switches/38._note`: Controller.Switch on/off
- `games/austin.json#/switches/39._note`: Controller.Switch on/off
- `games/austin.json#/switches/40._note`: PulseSw 59 in LeftSlingShot_Slingshot sub
- `games/austin.json#/switches/41._note`: Controller.Switch on/off
- `games/austin.json#/switches/42._note`: Controller.Switch on/off
- `games/austin.json#/switches/43._note`: PulseSw 62 in RightSlingShot_Slingshot sub
- `games/austin.json#/coils/0._vbscript_callback`: SolTrough
- `games/austin.json#/coils/0._inferred_type`: ball_management
- `games/austin.json#/coils/0._note`: Fires bsTrough.ExitSol_On, then PulseSw 15 (shooter lane confirm)
- `games/austin.json#/coils/1._vbscript_callback`: SolAutoPlungerIM
- `games/austin.json#/coils/1._inferred_type`: ball_management
- `games/austin.json#/coils/1._note`: Impulse plunger. plungerIM.AutoFire
- `games/austin.json#/coils/2._vbscript_callback`: bsScoop.SolOut
- `games/austin.json#/coils/2._inferred_type`: ball_management
- `games/austin.json#/coils/3._vbscript_callback`: SolLaserBeam
- `games/austin.json#/coils/3._inferred_type`: ball_management
- `games/austin.json#/coils/3._note`: Kicks ball from cannon. Clears Controller.switch(45).
- `games/austin.json#/coils/4._vbscript_callback`: SetLamp 105,
- `games/austin.json#/coils/4._inferred_type`: flasher
- `games/austin.json#/coils/5._vbscript_callback`: FlashGreen
- `games/austin.json#/coils/5._inferred_type`: flasher
- `games/austin.json#/coils/6._vbscript_callback`: SolAustinDance
- `games/austin.json#/coils/6._inferred_type`: mechanism
- `games/austin.json#/coils/6._note`: Activates Austin Powers dancing figure animation
- `games/austin.json#/coils/7._vbscript_callback`: bsInodoro.SolOut
- `games/austin.json#/coils/7._inferred_type`: ball_management
- `games/austin.json#/coils/8._vbscript_callback`: FlashBlue
- `games/austin.json#/coils/8._inferred_type`: flasher
- `games/austin.json#/coils/9._vbscript_callback`: FlashRed
- `games/austin.json#/coils/9._inferred_type`: flasher
- `games/austin.json#/coils/10._inferred_type`: mechanism
- `games/austin.json#/coils/10._note`: cvpmMagnet. GrabCenter = 1.
- `games/austin.json#/coils/11._vbscript_callback`: mrEvil
- `games/austin.json#/coils/11._inferred_type`: mechanism
- `games/austin.json#/coils/11._note`: cvpmMyMech. Dr Evil pop-up figure motor. Mech switches: sw23 (home 0-1), sw22 (top 498-500).
- `games/austin.json#/coils/12._vbscript_callback`: SolTimeMachine
- `games/austin.json#/coils/12._inferred_type`: mechanism
- `games/austin.json#/coils/12._note`: Time Machine Motor Relay Board
- `games/austin.json#/coils/13._vbscript_callback`: Solcannon
- `games/austin.json#/coils/13._inferred_type`: mechanism
- `games/austin.json#/coils/13._note`: cvpmMyMech. Rotates cannon/laser gun. Mech switches: sw43 (home 0-10), sw44 (end 400-750).
- `games/austin.json#/coils/14._vbscript_callback`: SolDiv
- `games/austin.json#/coils/14._inferred_type`: diverter
- `games/austin.json#/coils/15._vbscript_callback`: vpmSolGate Gate
- `games/austin.json#/coils/15._inferred_type`: gate
- `games/austin.json#/coils/16._vbscript_callback`: vpmSolSound SoundFX("fx_knocker",DOFKnocker),
- `games/austin.json#/coils/16._inferred_type`: knocker
- `games/austin.json#/coils/17._vbscript_callback`: SetLamp 125,
- `games/austin.json#/coils/17._inferred_type`: flasher
- `games/austin.json#/coils/18._vbscript_callback`: SetLamp 126,
- `games/austin.json#/coils/18._inferred_type`: flasher
- `games/austin.json#/coils/19._vbscript_callback`: SolFlasher27
- `games/austin.json#/coils/19._inferred_type`: flasher
- `games/austin.json#/coils/20._vbscript_callback`: SetLamp 128,
- `games/austin.json#/coils/20._inferred_type`: flasher
- `games/austin.json#/coils/21._vbscript_callback`: SetLamp 129,
- `games/austin.json#/coils/21._inferred_type`: flasher
- `games/austin.json#/coils/22._vbscript_callback`: SetLamp 130,
- `games/austin.json#/coils/22._inferred_type`: flasher
- `games/austin.json#/coils/23._vbscript_callback`: SetLamp 131,
- `games/austin.json#/coils/23._inferred_type`: flasher
- `games/austin.json#/coils/23._note`: Also has bloom effect object Flasherbloom31
- `games/austin.json#/coils/24._vbscript_callback`: FlashYellow
- `games/austin.json#/coils/24._inferred_type`: flasher
- `games/austin.json#/lamps/4._note`: Also has Flash object Light5a
- `games/austin.json#/lamps/5._note`: Also has Flash object Light6a
- `games/austin.json#/lamps/12._note`: Flash macro — bumper flasher
- `games/austin.json#/lamps/13._note`: Flash macro — bumper flasher
- `games/austin.json#/lamps/14._note`: Flash macro — bumper flasher
- `games/austin.json#/lamps/44._note`: Also has Flash object Light45a
- `games/austin.json#/lamps/47._note`: Also has Flash object Light48a
- `games/austin.json#/_source/confidence_notes`: High confidence on switches/coils. No Const sw* definitions — switches identified from _Hit/_UnHit subs, Controller.Switch() calls, PulseSw calls, and mechanism AddSw. Lamp IDs from NFadeL/Flash macros. Flashers (coils 5-6, 12-13, 25-32) use SetLamp with 100+ lamp IDs or custom Flash subs. Trough uses cvpmTrough with 4 switches (11-14). Sega/Whitestar platform via SEGA.VBS. Multiple mechanisms: LaserGun cannon (sol 21, mech), Dr Evil motor (sol 19, mech), Time Machine motor (sol 20), Dancing Austin (sol 7), Magnet (sol 14).

## Unresolved questions

- Is the I/O enumeration complete for every supported physical/controller variant?
- Which inferred VPX behaviors reflect real hardware, and which are table-script conveniences?
- Are all mechanism home states, sensors, motion constraints, and ball interactions documented?

## Sources

- `legacy.game.austin`: `games/austin.json` at the pinned migration revision.
