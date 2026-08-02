# Maverick

Coverage: **partial - source-derived recreation knowledge requiring validation**

## Overview

Legacy evidence identifies this candidate as Data East (1994). The information below is preserved for recreation work but is not automatically treated as validated physical-machine fact.

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

- `games/maverick.json#/switches/0._vbscript_callback`: vpmNudge.TiltSwitch = 1
- `games/maverick.json#/switches/0._inferred_type`: tilt
- `games/maverick.json#/switches/1._vbscript_callback`: bsTrough.InitSw position 4 / Drain_Hit sets Controller.Switch(11)=1
- `games/maverick.json#/switches/1._inferred_type`: trough
- `games/maverick.json#/switches/1._note`: Last position in InitSw (0,14,13,12,11,0,0,0). Also directly set in Drain_Hit.
- `games/maverick.json#/switches/2._vbscript_callback`: bsTrough.InitSw position 3
- `games/maverick.json#/switches/2._inferred_type`: trough
- `games/maverick.json#/switches/3._vbscript_callback`: bsTrough.InitSw position 2
- `games/maverick.json#/switches/3._inferred_type`: trough
- `games/maverick.json#/switches/4._vbscript_callback`: bsTrough.InitSw position 1
- `games/maverick.json#/switches/4._inferred_type`: trough
- `games/maverick.json#/switches/5._vbscript_callback`: bsTroughKick.InitSaucer BallRelease,15,80,8
- `games/maverick.json#/switches/5._inferred_type`: trough
- `games/maverick.json#/switches/6._vbscript_callback`: Controller.Switch(16)=1/0
- `games/maverick.json#/switches/6._inferred_type`: lane
- `games/maverick.json#/switches/7._vbscript_callback`: DTHit 17
- `games/maverick.json#/switches/7._inferred_type`: drop_target
- `games/maverick.json#/switches/8._vbscript_callback`: DTHit 18
- `games/maverick.json#/switches/8._inferred_type`: drop_target
- `games/maverick.json#/switches/9._vbscript_callback`: DTHit 19
- `games/maverick.json#/switches/9._inferred_type`: drop_target
- `games/maverick.json#/switches/10._vbscript_callback`: DTHit 20
- `games/maverick.json#/switches/10._inferred_type`: drop_target
- `games/maverick.json#/switches/11._vbscript_callback`: DTHit 21
- `games/maverick.json#/switches/11._inferred_type`: drop_target
- `games/maverick.json#/switches/12._vbscript_callback`: DTHit 22
- `games/maverick.json#/switches/12._inferred_type`: drop_target
- `games/maverick.json#/switches/13._vbscript_callback`: DTHit 23
- `games/maverick.json#/switches/13._inferred_type`: drop_target
- `games/maverick.json#/switches/14._vbscript_callback`: DTHit 24
- `games/maverick.json#/switches/14._inferred_type`: drop_target
- `games/maverick.json#/switches/15._vbscript_callback`: DTHit 25
- `games/maverick.json#/switches/15._inferred_type`: drop_target
- `games/maverick.json#/switches/16._vbscript_callback`: DTHit 26
- `games/maverick.json#/switches/16._inferred_type`: drop_target
- `games/maverick.json#/switches/17._vbscript_callback`: DTHit 27
- `games/maverick.json#/switches/17._inferred_type`: drop_target
- `games/maverick.json#/switches/18._vbscript_callback`: DTHit 28
- `games/maverick.json#/switches/18._inferred_type`: drop_target
- `games/maverick.json#/switches/19._vbscript_callback`: DTHit 29
- `games/maverick.json#/switches/19._inferred_type`: drop_target
- `games/maverick.json#/switches/20._vbscript_callback`: vpmTimer.PulseSw 30
- `games/maverick.json#/switches/20._inferred_type`: target
- `games/maverick.json#/switches/21._vbscript_callback`: Controller.Switch(31)=True in TopVUK_Hit
- `games/maverick.json#/switches/21._inferred_type`: vuk
- `games/maverick.json#/switches/22._vbscript_callback`: vpmTimer.PulseSw 32
- `games/maverick.json#/switches/22._inferred_type`: target
- `games/maverick.json#/switches/23._vbscript_callback`: DTHit 33
- `games/maverick.json#/switches/23._inferred_type`: drop_target
- `games/maverick.json#/switches/24._vbscript_callback`: DTHit 34
- `games/maverick.json#/switches/24._inferred_type`: drop_target
- `games/maverick.json#/switches/25._vbscript_callback`: DTHit 35
- `games/maverick.json#/switches/25._inferred_type`: drop_target
- `games/maverick.json#/switches/26._vbscript_callback`: DTHit 36
- `games/maverick.json#/switches/26._inferred_type`: drop_target
- `games/maverick.json#/switches/27._vbscript_callback`: Controller.Switch(37)=1/0
- `games/maverick.json#/switches/27._inferred_type`: lane
- `games/maverick.json#/switches/27._note`: Raised by SolRDTBank (DTRaise 37) with the right bank, but uses Hit/UnHit pattern instead of DTHit -- may be a standup target or rollover at end of the bank
- `games/maverick.json#/switches/28._vbscript_callback`: Controller.Switch(38)=1/0
- `games/maverick.json#/switches/28._inferred_type`: lane
- `games/maverick.json#/switches/29._vbscript_callback`: Controller.Switch(39)=1/0
- `games/maverick.json#/switches/29._inferred_type`: lane
- `games/maverick.json#/switches/30._vbscript_callback`: Controller.Switch(40)=1/0
- `games/maverick.json#/switches/30._inferred_type`: lane
- `games/maverick.json#/switches/31._vbscript_callback`: vpmTimer.PulseSw 41
- `games/maverick.json#/switches/31._inferred_type`: bumper
- `games/maverick.json#/switches/32._vbscript_callback`: vpmTimer.PulseSw 42
- `games/maverick.json#/switches/32._inferred_type`: bumper
- `games/maverick.json#/switches/33._vbscript_callback`: vpmTimer.PulseSw 43
- `games/maverick.json#/switches/33._inferred_type`: bumper
- `games/maverick.json#/switches/34._vbscript_callback`: vpmTimer.PulseSw 44
- `games/maverick.json#/switches/34._inferred_type`: target
- `games/maverick.json#/switches/35._vbscript_callback`: vLock.InitVlock position 2 (switch 45)
- `games/maverick.json#/switches/35._inferred_type`: lock
- `games/maverick.json#/switches/36._vbscript_callback`: vLock.InitVlock position 1 (switch 46)
- `games/maverick.json#/switches/36._inferred_type`: lock
- `games/maverick.json#/switches/37._vbscript_callback`: Controller.Switch(47)=1/0
- `games/maverick.json#/switches/37._inferred_type`: lane
- `games/maverick.json#/switches/38._vbscript_callback`: Controller.Switch(49)=1/0
- `games/maverick.json#/switches/38._inferred_type`: lane
- `games/maverick.json#/switches/39._vbscript_callback`: vpmTimer.PulseSw 50
- `games/maverick.json#/switches/39._inferred_type`: target
- `games/maverick.json#/switches/40._vbscript_callback`: vpmTimer.PulseSw 51
- `games/maverick.json#/switches/40._inferred_type`: slingshot
- `games/maverick.json#/switches/41._vbscript_callback`: Controller.Switch(52)=1/0
- `games/maverick.json#/switches/41._inferred_type`: lane
- `games/maverick.json#/switches/42._vbscript_callback`: Controller.Switch(53)=1/0
- `games/maverick.json#/switches/42._inferred_type`: lane
- `games/maverick.json#/switches/43._vbscript_callback`: Controller.Switch(54)=1/0
- `games/maverick.json#/switches/43._inferred_type`: lane
- `games/maverick.json#/switches/44._vbscript_callback`: Controller.Switch(55)=1/0
- `games/maverick.json#/switches/44._inferred_type`: lane
- `games/maverick.json#/switches/45._vbscript_callback`: vpmTimer.PulseSw 56
- `games/maverick.json#/switches/45._inferred_type`: target
- `games/maverick.json#/switches/46._vbscript_callback`: Controller.Switch(57)=1/0
- `games/maverick.json#/switches/46._inferred_type`: lane
- `games/maverick.json#/switches/47._vbscript_callback`: vpmTimer.PulseSw 58
- `games/maverick.json#/switches/47._inferred_type`: target
- `games/maverick.json#/switches/48._vbscript_callback`: vpmTimer.PulseSw 59
- `games/maverick.json#/switches/48._inferred_type`: slingshot
- `games/maverick.json#/switches/49._vbscript_callback`: Controller.Switch(60)=1/0
- `games/maverick.json#/switches/49._inferred_type`: lane
- `games/maverick.json#/switches/50._vbscript_callback`: Controller.Switch(61)=1/0
- `games/maverick.json#/switches/50._inferred_type`: lane
- `games/maverick.json#/switches/51._vbscript_callback`: Controller.Switch(62)=1/0
- `games/maverick.json#/switches/51._inferred_type`: lane
- `games/maverick.json#/coils/0._vbscript_callback`: SolLockout
- `games/maverick.json#/coils/0._inferred_type`: ball_management
- `games/maverick.json#/coils/0._note`: Calls bsTrough.ExitSol_On and creates ball at BallRelease
- `games/maverick.json#/coils/1._vbscript_callback`: bsTroughKick.SolOut
- `games/maverick.json#/coils/1._inferred_type`: ball_management
- `games/maverick.json#/coils/2._vbscript_callback`: SolSkillshot
- `games/maverick.json#/coils/2._inferred_type`: kicker
- `games/maverick.json#/coils/3._vbscript_callback`: SolLUBankAuto
- `games/maverick.json#/coils/3._inferred_type`: drop_target_reset
- `games/maverick.json#/coils/3._note`: Drops sw25-29 down (autodrop feature)
- `games/maverick.json#/coils/4._vbscript_callback`: SolLUBank
- `games/maverick.json#/coils/4._inferred_type`: drop_target_reset
- `games/maverick.json#/coils/4._note`: Raises sw25-29
- `games/maverick.json#/coils/5._vbscript_callback`: SolCDTBank
- `games/maverick.json#/coils/5._inferred_type`: drop_target_reset
- `games/maverick.json#/coils/5._note`: Raises sw22-24
- `games/maverick.json#/coils/6._vbscript_callback`: SolRDTBank
- `games/maverick.json#/coils/6._inferred_type`: drop_target_reset
- `games/maverick.json#/coils/6._note`: Raises sw33-37 (script comment says 4-Bank but code raises 5 targets)
- `games/maverick.json#/coils/7._vbscript_callback`: vpmSolSound SoundFX("Knocker_1",DOFKnocker),
- `games/maverick.json#/coils/7._inferred_type`: knocker
- `games/maverick.json#/coils/8._vbscript_callback`: SolRdiv
- `games/maverick.json#/coils/8._inferred_type`: diverter
- `games/maverick.json#/coils/9._vbscript_callback`: GIRelay
- `games/maverick.json#/coils/9._inferred_type`: gi_relay
- `games/maverick.json#/coils/10._vbscript_callback`: LockRelease
- `games/maverick.json#/coils/10._inferred_type`: ball_management
- `games/maverick.json#/coils/10._note`: Calls vLock.SolExit to release locked balls
- `games/maverick.json#/coils/11._vbscript_callback`: SolLDTLwrBank
- `games/maverick.json#/coils/11._inferred_type`: drop_target_reset
- `games/maverick.json#/coils/11._note`: Raises sw17-21
- `games/maverick.json#/coils/12._vbscript_callback`: VukTopPop
- `games/maverick.json#/coils/12._inferred_type`: kicker
- `games/maverick.json#/coils/13._vbscript_callback`: SolBallDeflector
- `games/maverick.json#/coils/13._inferred_type`: diverter
- `games/maverick.json#/coils/14._vbscript_callback`: SolWheel
- `games/maverick.json#/coils/14._inferred_type`: mechanism
- `games/maverick.json#/coils/14._note`: Rotating paddle wheel mechanism with ball capture/release
- `games/maverick.json#/coils/15._vbscript_callback`: commented out: vpmSolSound "jet3",
- `games/maverick.json#/coils/15._inferred_type`: bumper
- `games/maverick.json#/coils/15._note`: Commented out in script -- bumper physics handled by VPX
- `games/maverick.json#/coils/16._vbscript_callback`: commented out: vpmSolSound "jet3",
- `games/maverick.json#/coils/16._inferred_type`: bumper
- `games/maverick.json#/coils/16._note`: Commented out in script -- bumper physics handled by VPX
- `games/maverick.json#/coils/17._vbscript_callback`: commented out: vpmSolSound "jet3",
- `games/maverick.json#/coils/17._inferred_type`: bumper
- `games/maverick.json#/coils/17._note`: Commented out in script -- bumper physics handled by VPX
- `games/maverick.json#/coils/18._vbscript_callback`: commented out: vpmSolSound "Sling",
- `games/maverick.json#/coils/18._inferred_type`: slingshot
- `games/maverick.json#/coils/18._note`: Commented out in script -- slingshot physics handled by VPX
- `games/maverick.json#/coils/19._vbscript_callback`: commented out: vpmSolSound "Sling",
- `games/maverick.json#/coils/19._inferred_type`: slingshot
- `games/maverick.json#/coils/19._note`: Commented out in script -- slingshot physics handled by VPX
- `games/maverick.json#/coils/20._vbscript_callback`: SolKickBack
- `games/maverick.json#/coils/20._inferred_type`: kicker
- `games/maverick.json#/coils/21._vbscript_callback`: FlashSkill
- `games/maverick.json#/coils/21._inferred_type`: flasher
- `games/maverick.json#/coils/21._note`: Sets lamp 125 and fires flasher objects 1 & 2
- `games/maverick.json#/coils/22._vbscript_callback`: JokersFlash
- `games/maverick.json#/coils/22._inferred_type`: flasher
- `games/maverick.json#/coils/22._note`: Sets lamp 126 and fires flasher object 6
- `games/maverick.json#/coils/23._vbscript_callback`: SetLamp 127,
- `games/maverick.json#/coils/23._inferred_type`: flasher
- `games/maverick.json#/coils/24._vbscript_callback`: FlashPaddle
- `games/maverick.json#/coils/24._inferred_type`: flasher
- `games/maverick.json#/coils/24._note`: Sets lamp 128 and fires flasher object 5
- `games/maverick.json#/coils/25._vbscript_callback`: FlashLLeft
- `games/maverick.json#/coils/25._inferred_type`: flasher
- `games/maverick.json#/coils/25._note`: Sets lamp 129 and fires flasher objects 3 & 4
- `games/maverick.json#/coils/26._vbscript_callback`: SetLamp 130,
- `games/maverick.json#/coils/26._inferred_type`: flasher
- `games/maverick.json#/coils/27._vbscript_callback`: SetLamp 131,
- `games/maverick.json#/coils/27._inferred_type`: flasher
- `games/maverick.json#/coils/28._vbscript_callback`: SetLamp 132,
- `games/maverick.json#/coils/28._inferred_type`: flasher
- `games/maverick.json#/coils/29._vbscript_name`: sURFlipper
- `games/maverick.json#/coils/29._vbscript_callback`: SolURFlipper
- `games/maverick.json#/coils/29._inferred_type`: flipper
- `games/maverick.json#/coils/30._vbscript_name`: sLRFlipper
- `games/maverick.json#/coils/30._vbscript_callback`: SolRFlipper
- `games/maverick.json#/coils/30._inferred_type`: flipper
- `games/maverick.json#/coils/31._vbscript_name`: sLLFlipper
- `games/maverick.json#/coils/31._vbscript_callback`: SolLFlipper
- `games/maverick.json#/coils/31._inferred_type`: flipper
- `games/maverick.json#/lamps/0._inferred_type`: insert
- `games/maverick.json#/lamps/1._inferred_type`: insert
- `games/maverick.json#/lamps/2._inferred_type`: insert
- `games/maverick.json#/lamps/3._inferred_type`: insert
- `games/maverick.json#/lamps/4._inferred_type`: insert
- `games/maverick.json#/lamps/5._inferred_type`: insert
- `games/maverick.json#/lamps/6._inferred_type`: insert
- `games/maverick.json#/lamps/7._inferred_type`: insert
- `games/maverick.json#/lamps/8._inferred_type`: flasher
- `games/maverick.json#/lamps/9._inferred_type`: insert
- `games/maverick.json#/lamps/10._inferred_type`: insert
- `games/maverick.json#/lamps/11._inferred_type`: insert
- `games/maverick.json#/lamps/11._note`: Multi-light with PrimL12 primitive
- `games/maverick.json#/lamps/12._inferred_type`: insert
- `games/maverick.json#/lamps/13._inferred_type`: insert
- `games/maverick.json#/lamps/14._inferred_type`: insert
- `games/maverick.json#/lamps/15._inferred_type`: insert
- `games/maverick.json#/lamps/16._inferred_type`: insert
- `games/maverick.json#/lamps/17._inferred_type`: insert
- `games/maverick.json#/lamps/18._inferred_type`: insert
- `games/maverick.json#/lamps/19._inferred_type`: insert
- `games/maverick.json#/lamps/20._inferred_type`: insert
- `games/maverick.json#/lamps/21._inferred_type`: insert
- `games/maverick.json#/lamps/22._inferred_type`: insert
- `games/maverick.json#/lamps/23._inferred_type`: insert
- `games/maverick.json#/lamps/23._note`: Multi-light: L25, L25a, Primitive023
- `games/maverick.json#/lamps/24._inferred_type`: insert
- `games/maverick.json#/lamps/24._note`: Multi-light: L26, L26a, Primitive024
- `games/maverick.json#/lamps/25._inferred_type`: insert
- `games/maverick.json#/lamps/25._note`: Multi-light: L27, L27a, Primitive7
- `games/maverick.json#/lamps/26._inferred_type`: insert
- `games/maverick.json#/lamps/27._inferred_type`: insert
- `games/maverick.json#/lamps/28._inferred_type`: insert
- `games/maverick.json#/lamps/29._inferred_type`: insert
- `games/maverick.json#/lamps/30._inferred_type`: insert
- `games/maverick.json#/lamps/31._inferred_type`: insert
- `games/maverick.json#/lamps/31._note`: FDL primitive-only lamp (no VPX light)
- `games/maverick.json#/lamps/32._inferred_type`: insert
- `games/maverick.json#/lamps/32._note`: FDL primitive-only lamp (no VPX light)
- `games/maverick.json#/lamps/33._inferred_type`: insert
- `games/maverick.json#/lamps/33._note`: FDL primitive-only lamp (no VPX light)
- `games/maverick.json#/lamps/34._inferred_type`: insert
- `games/maverick.json#/lamps/34._note`: Multi-light: L37a, L37b
- `games/maverick.json#/lamps/35._inferred_type`: insert
- `games/maverick.json#/lamps/36._inferred_type`: insert
- `games/maverick.json#/lamps/37._inferred_type`: insert
- `games/maverick.json#/lamps/38._inferred_type`: insert
- `games/maverick.json#/lamps/39._inferred_type`: insert
- `games/maverick.json#/lamps/40._inferred_type`: insert
- `games/maverick.json#/lamps/41._inferred_type`: insert
- `games/maverick.json#/lamps/42._inferred_type`: insert
- `games/maverick.json#/lamps/43._inferred_type`: insert
- `games/maverick.json#/lamps/43._note`: Multi-light: L46a, L46b
- `games/maverick.json#/lamps/44._inferred_type`: insert
- `games/maverick.json#/lamps/45._inferred_type`: insert
- `games/maverick.json#/lamps/46._inferred_type`: insert
- `games/maverick.json#/lamps/47._inferred_type`: insert
- `games/maverick.json#/lamps/48._inferred_type`: insert
- `games/maverick.json#/lamps/49._inferred_type`: insert
- `games/maverick.json#/lamps/49._note`: Multi-light with PrimL52 primitive
- `games/maverick.json#/lamps/50._inferred_type`: insert
- `games/maverick.json#/lamps/51._inferred_type`: insert
- `games/maverick.json#/lamps/52._inferred_type`: insert
- `games/maverick.json#/lamps/52._note`: Multi-light: L55a, L55b
- `games/maverick.json#/lamps/53._inferred_type`: insert
- `games/maverick.json#/lamps/54._inferred_type`: insert
- `games/maverick.json#/lamps/55._inferred_type`: insert
- `games/maverick.json#/lamps/56._inferred_type`: insert
- `games/maverick.json#/lamps/57._inferred_type`: insert
- `games/maverick.json#/lamps/58._inferred_type`: insert
- `games/maverick.json#/lamps/59._inferred_type`: insert
- `games/maverick.json#/lamps/60._inferred_type`: flasher
- `games/maverick.json#/lamps/60._note`: Driven by sol 25 (FlashSkill). Multi-light: L125, L125a, f125, f125a, Primitive088
- `games/maverick.json#/lamps/61._inferred_type`: flasher
- `games/maverick.json#/lamps/61._note`: Driven by sol 26 (JokersFlash)
- `games/maverick.json#/lamps/62._inferred_type`: flasher
- `games/maverick.json#/lamps/62._note`: Driven by sol 27. Multi-light: L127, L127a, L127b, F127, F127a, F127b
- `games/maverick.json#/lamps/63._inferred_type`: flasher
- `games/maverick.json#/lamps/63._note`: Driven by sol 28 (FlashPaddle). Multi-light: L128, L128a, F128
- `games/maverick.json#/lamps/64._inferred_type`: flasher
- `games/maverick.json#/lamps/64._note`: Driven by sol 29 (FlashLLeft)
- `games/maverick.json#/lamps/65._inferred_type`: flasher
- `games/maverick.json#/lamps/65._note`: Driven by sol 30. Multi-light: L130, f130
- `games/maverick.json#/lamps/66._inferred_type`: flasher
- `games/maverick.json#/lamps/66._note`: Driven by sol 31. Multi-light: L131, f131
- `games/maverick.json#/lamps/67._inferred_type`: flasher
- `games/maverick.json#/lamps/67._note`: Driven by sol 32. Multi-light: L132, L132a, f132, f132a
- `games/maverick.json#/_source/confidence_notes`: High confidence. Switch layout from bsTrough.InitSw (sw11-14), bsTroughKick.InitSaucer (sw15), vLock (sw45/46), TopVUK (sw31), and Controller.Switch/PulseSw/DTHit handlers. No Const sw* definitions in table script -- switches referenced by number or VPX object name. Lamp IDs from UpdateLamps function (Lamp/Lampm/Flash calls). Flasher-lamps 125-132 driven by SetLamp from solenoid callbacks. DE framework flipper constants sLRFlipper=46, sLLFlipper=48, sURFlipper=34 from DE.VBS. GI controlled by sol 11 relay. Bumper solenoids 17-19 and slingshot solenoids 20-21 commented out in script (handled by VPX physics). TiltSwitch=1. IPDB link in script header: id=1561.

## Unresolved questions

- Is the I/O enumeration complete for every supported physical/controller variant?
- Which inferred VPX behaviors reflect real hardware, and which are table-script conveniences?
- Are all mechanism home states, sensors, motion constraints, and ball interactions documented?

## Sources

- `legacy.game.maverick`: `games/maverick.json` at the pinned migration revision.
