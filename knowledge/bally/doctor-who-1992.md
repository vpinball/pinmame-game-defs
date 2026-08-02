# Doctor Who

Coverage: **partial - source-derived recreation knowledge requiring validation**

## Overview

Legacy evidence identifies this candidate as Bally (1992). The information below is preserved for recreation work but is not automatically treated as validated physical-machine fact.

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
- `games/dw.json#/switches/0._note`: vpmNudge.TiltSwitch = 14
- `games/dw.json#/switches/1._inferred_type`: slingshot
- `games/dw.json#/switches/1._note`: PulseSw 15 in LeftSling_Slingshot
- `games/dw.json#/switches/2._inferred_type`: slingshot
- `games/dw.json#/switches/2._note`: PulseSw 16 in RightSling_Slingshot
- `games/dw.json#/switches/4._note`: PulseSw 18
- `games/dw.json#/switches/5._note`: Controller.Switch(22) = 1 in Table1_Init
- `games/dw.json#/switches/6._note`: Controller.Switch(24) = 1 in Table1_Init
- `games/dw.json#/switches/11._note`: TardisEntrance_hit sets switch 31; TardisExit solenoid clears it
- `games/dw.json#/switches/12._note`: Controlled by UpdateMiniPF mechanism callback based on aCurrPos
- `games/dw.json#/switches/13._note`: PulseSw 33
- `games/dw.json#/switches/14._note`: Controller.Switch(34) toggled by PlungerKey
- `games/dw.json#/switches/15._note`: PulseSw 35
- `games/dw.json#/switches/16._note`: PulseSw 36
- `games/dw.json#/switches/17._note`: PulseSw 37
- `games/dw.json#/switches/18._note`: PulseSw 38
- `games/dw.json#/switches/26._note`: PulseSw 48
- `games/dw.json#/switches/33._note`: Opto controlled by TDUpTimer_timer based on trap door position
- `games/dw.json#/switches/35._note`: PulseSw 61
- `games/dw.json#/switches/36._note`: PulseSw 62
- `games/dw.json#/switches/37._note`: PulseSw 63
- `games/dw.json#/switches/42._note`: PulseSw 68
- `games/dw.json#/switches/51._note`: Controller.Switch(82) = 1 in Table1_Init
- `games/dw.json#/switches/52._note`: PulseSw 88
- `games/dw.json#/coils/0._vbscript_callback`: SolTrapDoor
- `games/dw.json#/coils/0._inferred_type`: mechanism
- `games/dw.json#/coils/0._note`: Controls trap door collidable state and TDUpTimer animation. Drives sw57 open/close.
- `games/dw.json#/coils/1._vbscript_callback`: SolAutoFire
- `games/dw.json#/coils/1._inferred_type`: ball_management
- `games/dw.json#/coils/1._note`: Impulse plunger auto-fire via PlungerIM.AutoFire
- `games/dw.json#/coils/2._vbscript_callback`: TardisExit
- `games/dw.json#/coils/2._inferred_type`: kicker
- `games/dw.json#/coils/2._note`: Kicks ball out of Tardis VUK; clears sw31
- `games/dw.json#/coils/3._vbscript_callback`: solmpfl
- `games/dw.json#/coils/3._inferred_type`: kicker
- `games/dw.json#/coils/4._vbscript_callback`: solmpfr
- `games/dw.json#/coils/4._inferred_type`: kicker
- `games/dw.json#/coils/5._vbscript_callback`: Flash06
- `games/dw.json#/coils/5._inferred_type`: flasher
- `games/dw.json#/coils/5._note`: SolModCallback — PWM fading. VPX objects: FL06, FL06b, FL06h
- `games/dw.json#/coils/6._vbscript_callback`: SolKnocker
- `games/dw.json#/coils/6._inferred_type`: knocker
- `games/dw.json#/coils/7._vbscript_callback`: Flash08
- `games/dw.json#/coils/7._inferred_type`: flasher
- `games/dw.json#/coils/7._note`: SolModCallback — PWM fading. Backbox flasher only (FL8bg)
- `games/dw.json#/coils/8._inferred_type`: bumper
- `games/dw.json#/coils/8._note`: SolCallback commented out in script (bpr1)
- `games/dw.json#/coils/9._inferred_type`: bumper
- `games/dw.json#/coils/9._note`: SolCallback commented out in script (bpr2)
- `games/dw.json#/coils/10._inferred_type`: bumper
- `games/dw.json#/coils/10._note`: SolCallback commented out in script (bpr3)
- `games/dw.json#/coils/11._vbscript_callback`: SolOutHole
- `games/dw.json#/coils/11._inferred_type`: ball_management
- `games/dw.json#/coils/12._vbscript_callback`: SolBallRelease
- `games/dw.json#/coils/12._inferred_type`: ball_management
- `games/dw.json#/coils/13._vbscript_callback`: Flash17
- `games/dw.json#/coils/13._inferred_type`: flasher
- `games/dw.json#/coils/13._note`: SolModCallback — PWM fading. VPX objects: FL17, TEFlashP
- `games/dw.json#/coils/14._vbscript_callback`: Flash18
- `games/dw.json#/coils/14._inferred_type`: flasher
- `games/dw.json#/coils/14._note`: SolModCallback — PWM fading. VPX object: FL18
- `games/dw.json#/coils/15._vbscript_callback`: Flash19
- `games/dw.json#/coils/15._inferred_type`: flasher
- `games/dw.json#/coils/15._note`: SolModCallback — PWM fading. VPX object: FL19
- `games/dw.json#/coils/16._vbscript_callback`: Flash20
- `games/dw.json#/coils/16._inferred_type`: flasher
- `games/dw.json#/coils/16._note`: SolModCallback — PWM fading. VPX object: FL20 (opacity-based)
- `games/dw.json#/coils/17._vbscript_callback`: Flash21
- `games/dw.json#/coils/17._inferred_type`: flasher
- `games/dw.json#/coils/17._note`: SolModCallback — PWM fading. VPX objects: FL21, FL21b, RepairFlash
- `games/dw.json#/coils/18._vbscript_callback`: who_h
- `games/dw.json#/coils/18._inferred_type`: flasher
- `games/dw.json#/coils/18._note`: SolModCallback — PWM fading. VPX objects: FL22, FL22h
- `games/dw.json#/coils/19._vbscript_callback`: who_o
- `games/dw.json#/coils/19._inferred_type`: flasher
- `games/dw.json#/coils/19._note`: SolModCallback — PWM fading. VPX objects: FL23, FL23h
- `games/dw.json#/coils/20._vbscript_callback`: Flash24
- `games/dw.json#/coils/20._inferred_type`: flasher
- `games/dw.json#/coils/20._note`: SolModCallback — PWM fading. VPX objects: FL24, EscapeFlash
- `games/dw.json#/coils/21._inferred_type`: mechanism
- `games/dw.json#/coils/21._note`: cvpmmech sol2 — mini-playfield raise/lower mechanism direction 2
- `games/dw.json#/coils/22._vbscript_callback`: TEOnOff
- `games/dw.json#/coils/22._inferred_type`: mechanism
- `games/dw.json#/coils/22._note`: cvpmmech sol1 — mini-playfield raise/lower mechanism direction 1; TEOnOff sets TEOn flag
- `games/dw.json#/lamps/46._note`: Uses flasher object (fl67) not standard light
- `games/dw.json#/lamps/61._note`: Dual lamp: l86a and l86b
- `games/dw.json#/lamps/62._note`: Launch Button lamp — f87 in non-VR, callback in VR mode
- `games/dw.json#/lamps/63._note`: Start Button lamp — f88 in non-VR, f88f flasher in VR mode
- `games/dw.json#/_source/confidence_notes`: High confidence on switches/coils from VBScript handlers, Controller.Switch() calls, and PulseSw calls. Lamp IDs from Lampz.MassAssign() calls. Flasher coils (6,8,17-24) use SolModCallback for PWM fading. Mini-playfield mechanism uses sol1=28, sol2=27 via cvpmmech. Three flippers: left (sLLFlipper), right (sLRFlipper), upper left (sULFlipper). Jet bumper SolCallbacks (11-13) commented out in script. No Const sw* definitions — switches referenced directly by number. Trough is custom (3 ball + outhole), not bsTrough.

## Unresolved questions

- Is the I/O enumeration complete for every supported physical/controller variant?
- Which inferred VPX behaviors reflect real hardware, and which are table-script conveniences?
- Are all mechanism home states, sensors, motion constraints, and ball interactions documented?

## Sources

- `legacy.game.dw`: `games/dw.json` at the pinned migration revision.
