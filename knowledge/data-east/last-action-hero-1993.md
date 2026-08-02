# Last Action Hero

Coverage: **partial - source-derived recreation knowledge requiring validation**

## Overview

Legacy evidence identifies this candidate as Data East (1993). The information below is preserved for recreation work but is not automatically treated as validated physical-machine fact.

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

- `games/lah.json#/switches/0._note`: vpmNudge.TiltSwitch=1
- `games/lah.json#/switches/1._note`: Set via PlungerKey in Table1_KeyDown
- `games/lah.json#/switches/8._note`: Virtual switch set by SolTrough/SolRelease, no VPX kicker object
- `games/lah.json#/switches/9._note`: Also used by cvpmImpulseP plunger (.Switch 16)
- `games/lah.json#/switches/15._note`: Lock post area — enables PostSettleTimer, triggers WireRampOff
- `games/lah.json#/switches/16._note`: Lock post area — enables PostSettleTimer
- `games/lah.json#/switches/24._note`: bsRScoop ball stack — InitSaucer sw31, solenoid 6
- `games/lah.json#/switches/26._note`: vpmTimer.PulseSw 33
- `games/lah.json#/switches/27._note`: vpmTimer.PulseSw 34
- `games/lah.json#/switches/28._note`: vpmTimer.PulseSw 35
- `games/lah.json#/switches/29._note`: vpmTimer.PulseSw 36
- `games/lah.json#/switches/30._note`: vpmTimer.PulseSw 37
- `games/lah.json#/switches/40._note`: bsVuk ball stack — InitSaucer sw47, solenoid 5
- `games/lah.json#/switches/41._note`: vpmTimer.PulseSw 48 — used as kicker by SolRipperKick (sol 22)
- `games/lah.json#/switches/42._note`: vpmTimer.PulseSw 54
- `games/lah.json#/switches/45._note`: bsMLScoop ball stack — InitSaucer sw57, solenoid 15
- `games/lah.json#/switches/46._note`: vpmTimer.PulseSw 58
- `games/lah.json#/switches/47._note`: Sw59_Spin — vpmTimer.PulseSw 59
- `games/lah.json#/switches/48._note`: Set by crane motor code — CraneIsLeft sets switch 60=1, CraneIsRight sets 60=0
- `games/lah.json#/switches/49._note`: Set by crane motor code — CraneIsRight sets switch 61=1, CraneIsLeft sets 61=0
- `games/lah.json#/switches/50._note`: Set via PlungerKey and LockBarKey in Table1_KeyDown — no physical VPX object
- `games/lah.json#/coils/0._vbscript_callback`: SolTrough
- `games/lah.json#/coils/0._inferred_type`: ball_management
- `games/lah.json#/coils/0._note`: Kicks from sw14 to sw15, sets Controller.Switch(15)=1
- `games/lah.json#/coils/1._vbscript_callback`: SolRelease
- `games/lah.json#/coils/1._inferred_type`: ball_management
- `games/lah.json#/coils/1._note`: Kicks from sw15 to shooter lane, sets Controller.Switch(15)=0
- `games/lah.json#/coils/2._vbscript_callback`: AutoLaunch
- `games/lah.json#/coils/2._inferred_type`: kicker
- `games/lah.json#/coils/2._note`: cvpmImpulseP auto-fire plunger
- `games/lah.json#/coils/3._vbscript_callback`: SolCraneLock
- `games/lah.json#/coils/3._inferred_type`: mechanism
- `games/lah.json#/coils/3._note`: Releases ball from crane when disabled and crane at left position (sw60)
- `games/lah.json#/coils/4._vbscript_callback`: bsVuk.SolOut
- `games/lah.json#/coils/4._inferred_type`: kicker
- `games/lah.json#/coils/4._note`: cvpmBallStack eject — InitSaucer sw47
- `games/lah.json#/coils/5._vbscript_callback`: bsRScoop.SolOut
- `games/lah.json#/coils/5._inferred_type`: kicker
- `games/lah.json#/coils/5._note`: cvpmBallStack eject — InitSaucer sw31
- `games/lah.json#/coils/6._vbscript_callback`: SolLockRelease
- `games/lah.json#/coils/6._inferred_type`: mechanism
- `games/lah.json#/coils/6._note`: Drops lock post to release ball
- `games/lah.json#/coils/7._vbscript_callback`: SolKnocker
- `games/lah.json#/coils/7._inferred_type`: knocker
- `games/lah.json#/coils/8._vbscript_callback`: Lampz.SetLamp 109,
- `games/lah.json#/coils/8._inferred_type`: flasher
- `games/lah.json#/coils/8._note`: Lampz index 109 — Crane(x2) + Backbox Inserts(x2)
- `games/lah.json#/coils/9._inferred_type`: relay
- `games/lah.json#/coils/9._note`: Commented out in VBScript — no callback assigned
- `games/lah.json#/coils/10._vbscript_callback`: SolGI
- `games/lah.json#/coils/10._inferred_type`: gi_relay
- `games/lah.json#/coils/10._note`: Controls GI lighting via Lampz.state(0) — inverted logic (enabled=off, disabled=on)
- `games/lah.json#/coils/11._vbscript_callback`: SolDiv
- `games/lah.json#/coils/11._inferred_type`: diverter
- `games/lah.json#/coils/12._vbscript_callback`: SoLDrop
- `games/lah.json#/coils/12._inferred_type`: drop_target_reset
- `games/lah.json#/coils/12._note`: Resets all 5 drop targets (sw17-sw21)
- `games/lah.json#/coils/13._vbscript_callback`: SoLCraneMotor
- `games/lah.json#/coils/13._inferred_type`: motor
- `games/lah.json#/coils/13._note`: Enables CraneTimer — drives crane left/right, sets sw60/sw61
- `games/lah.json#/coils/14._vbscript_callback`: bsMLScoop.SolOut
- `games/lah.json#/coils/14._inferred_type`: kicker
- `games/lah.json#/coils/14._note`: cvpmBallStack eject — InitSaucer sw57
- `games/lah.json#/coils/15._inferred_type`: motor
- `games/lah.json#/coils/15._note`: Commented out in VBScript — no callback assigned
- `games/lah.json#/coils/16._inferred_type`: bumper
- `games/lah.json#/coils/16._note`: Commented out in VBScript — bumpers handled by VPX physics
- `games/lah.json#/coils/17._inferred_type`: bumper
- `games/lah.json#/coils/17._note`: Commented out in VBScript — bumpers handled by VPX physics
- `games/lah.json#/coils/18._inferred_type`: bumper
- `games/lah.json#/coils/18._note`: Commented out in VBScript — bumpers handled by VPX physics
- `games/lah.json#/coils/19._inferred_type`: slingshot
- `games/lah.json#/coils/19._note`: Commented out in VBScript — slingshots handled by VPX physics
- `games/lah.json#/coils/20._inferred_type`: slingshot
- `games/lah.json#/coils/20._note`: Commented out in VBScript — slingshots handled by VPX physics
- `games/lah.json#/coils/21._vbscript_callback`: SolRipperKick
- `games/lah.json#/coils/21._inferred_type`: kicker
- `games/lah.json#/coils/21._note`: Kicks ball from sw48 kicker
- `games/lah.json#/coils/22._vbscript_callback`: Lampz.SetLamp 101,
- `games/lah.json#/coils/22._inferred_type`: flasher
- `games/lah.json#/coils/22._note`: Lampz index 101 — Topper Right Police(x4)
- `games/lah.json#/coils/23._vbscript_callback`: Lampz.SetLamp 102,
- `games/lah.json#/coils/23._inferred_type`: flasher
- `games/lah.json#/coils/23._note`: Lampz index 102 — Playfield Upper Left(x3) + Backbox Insert
- `games/lah.json#/coils/24._vbscript_callback`: Lampz.SetLamp 103,
- `games/lah.json#/coils/24._inferred_type`: flasher
- `games/lah.json#/coils/24._note`: Lampz index 103 — Ramp(x2) + Backbox Insert(x2)
- `games/lah.json#/coils/25._vbscript_callback`: Lampz.SetLamp 104,
- `games/lah.json#/coils/25._inferred_type`: flasher
- `games/lah.json#/coils/25._note`: Lampz index 104 — Playfield Upper Right(x2) + Backbox Insert(x2)
- `games/lah.json#/coils/26._vbscript_callback`: Lampz.SetLamp 105,
- `games/lah.json#/coils/26._inferred_type`: flasher
- `games/lah.json#/coils/26._note`: Lampz index 105 — Playfield Mid Right(x3) + Backbox Insert
- `games/lah.json#/coils/27._vbscript_callback`: Lampz.SetLamp 106,
- `games/lah.json#/coils/27._inferred_type`: flasher
- `games/lah.json#/coils/27._note`: Lampz index 106 — Playfield Low Right(x4)
- `games/lah.json#/coils/28._vbscript_callback`: Lampz.SetLamp 107,
- `games/lah.json#/coils/28._inferred_type`: flasher
- `games/lah.json#/coils/28._note`: Lampz index 107 — Topper Left Police(x4). MassAssign commented out in LampzHelper.
- `games/lah.json#/coils/29._vbscript_callback`: Lampz.SetLamp 108,
- `games/lah.json#/coils/29._inferred_type`: flasher
- `games/lah.json#/coils/29._note`: Lampz index 108 — Playfield Low Left + Backbox Insert(x2). MassAssign commented out in LampzHelper.
- `games/lah.json#/coils/30._vbscript_callback`: SolLeftMagnet
- `games/lah.json#/coils/30._inferred_type`: magnet
- `games/lah.json#/coils/30._note`: cvpmMagnet — InitMagnet LMagnet, strength 9
- `games/lah.json#/coils/31._vbscript_callback`: SolCenterMagnet
- `games/lah.json#/coils/31._inferred_type`: magnet
- `games/lah.json#/coils/31._note`: cvpmMagnet — InitMagnet CMagnet, strength 9
- `games/lah.json#/coils/32._vbscript_callback`: SolRightMagnet
- `games/lah.json#/coils/32._inferred_type`: magnet
- `games/lah.json#/coils/32._note`: cvpmMagnet — InitMagnet RMagnet, strength 9
- `games/lah.json#/coils/33._vbscript_name`: sLRFlipper
- `games/lah.json#/coils/33._vbscript_callback`: SolRFlipper
- `games/lah.json#/coils/33._inferred_type`: flipper
- `games/lah.json#/coils/34._vbscript_name`: sLLFlipper
- `games/lah.json#/coils/34._vbscript_callback`: SolLFlipper
- `games/lah.json#/coils/34._inferred_type`: flipper
- `games/lah.json#/lamps/0._note`: Controlled by SolGI (sol 11) — Lampz index 0, inverted logic
- `games/lah.json#/_source/confidence_notes`: High confidence on switches/coils from VPW VBScript. Trough is a 6-ball manual implementation (sw9-sw14, sw15 virtual). Switch descriptions are inferred from VBScript context (DTHit=drop target, STHit=standup, PulseSw=momentary, bsRScoop/bsVuk/bsMLScoop=ball stacks). Lamps l1-l63 are playfield inserts via Lampz.MassAssign. Flashers use Lampz indices 101-109 driven by SolCallback(9,25-32). GI is Lampz index 0, controlled by SolCallback(11) GI relay (inverted logic). Crane mechanism uses switches 60/61 for position and solenoids 4 (lock) and 14 (motor). Three magnets on solenoids 37-39. Flipper solenoids use framework constants sLRFlipper=46, sLLFlipper=48 from DE.VBS. No upper flippers on this game.

## Unresolved questions

- Is the I/O enumeration complete for every supported physical/controller variant?
- Which inferred VPX behaviors reflect real hardware, and which are table-script conveniences?
- Are all mechanism home states, sensors, motion constraints, and ball interactions documented?

## Sources

- `legacy.game.lah`: `games/lah.json` at the pinned migration revision.
