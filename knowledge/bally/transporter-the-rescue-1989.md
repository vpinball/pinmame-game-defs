# Transporter the Rescue

Coverage: **partial - source-derived recreation knowledge requiring validation**

## Overview

Legacy evidence identifies this candidate as Bally (1989). The information below is preserved for recreation work but is not automatically treated as validated physical-machine fact.

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

- `games/tran.json#/switches/5._note`: Held switch — cleared by PopperSol (coil 6)
- `games/tran.json#/switches/6._inferred_type`: standup_target
- `games/tran.json#/switches/6._note`: Pulsed via vpmTimer.PulseSw(16)
- `games/tran.json#/switches/7._note`: Held switch — ball velocity modified on entry
- `games/tran.json#/switches/8._inferred_type`: drop_target
- `games/tran.json#/switches/8._note`: Left bank — uses DTHit handler
- `games/tran.json#/switches/9._inferred_type`: drop_target
- `games/tran.json#/switches/9._note`: Left bank — uses DTHit handler
- `games/tran.json#/switches/10._inferred_type`: drop_target
- `games/tran.json#/switches/10._note`: Left bank — uses DTHit handler
- `games/tran.json#/switches/11._inferred_type`: drop_target
- `games/tran.json#/switches/11._note`: Right bank — uses DTHit handler
- `games/tran.json#/switches/12._inferred_type`: drop_target
- `games/tran.json#/switches/12._note`: Right bank — uses DTHit handler
- `games/tran.json#/switches/13._inferred_type`: drop_target
- `games/tran.json#/switches/13._note`: Right bank — uses DTHit handler
- `games/tran.json#/switches/17._inferred_type`: standup_target
- `games/tran.json#/switches/17._note`: Pulsed via vpmTimer.PulseSw(30)
- `games/tran.json#/switches/18._note`: Held switch — has speed-up helpers for ball velocity
- `games/tran.json#/switches/21._inferred_type`: spinner
- `games/tran.json#/switches/21._note`: Pulsed via vpmTimer.PulseSw(35)
- `games/tran.json#/switches/25._note`: Framework constant swTilt from S11.VBS
- `games/tran.json#/switches/27._inferred_type`: bumper
- `games/tran.json#/switches/27._note`: Bumper1 — pulsed via vpmTimer.PulseSw(60)
- `games/tran.json#/switches/28._inferred_type`: bumper
- `games/tran.json#/switches/28._note`: Bumper2 — pulsed via vpmTimer.PulseSw(61)
- `games/tran.json#/switches/29._inferred_type`: bumper
- `games/tran.json#/switches/29._note`: Bumper3 — pulsed via vpmTimer.PulseSw(62)
- `games/tran.json#/switches/30._inferred_type`: slingshot
- `games/tran.json#/switches/30._note`: Pulsed via vpmTimer.PulseSw(63)
- `games/tran.json#/switches/31._inferred_type`: slingshot
- `games/tran.json#/switches/31._note`: Pulsed via vpmTimer.PulseSw(64)
- `games/tran.json#/coils/0._vbscript_callback`: ballDrain
- `games/tran.json#/coils/0._inferred_type`: ball_management
- `games/tran.json#/coils/1._vbscript_callback`: BallKick
- `games/tran.json#/coils/1._inferred_type`: ball_management
- `games/tran.json#/coils/2._vbscript_callback`: dtLSolDropUp
- `games/tran.json#/coils/2._inferred_type`: drop_target_reset
- `games/tran.json#/coils/2._note`: Raises drop targets sw19, sw20, sw21
- `games/tran.json#/coils/3._vbscript_callback`: dtRSolDropUp
- `games/tran.json#/coils/3._inferred_type`: drop_target_reset
- `games/tran.json#/coils/3._note`: Raises drop targets sw22, sw23, sw24
- `games/tran.json#/coils/4._vbscript_callback`: LeftLockSol
- `games/tran.json#/coils/4._inferred_type`: ball_management
- `games/tran.json#/coils/4._note`: Fires LockLSol kicker
- `games/tran.json#/coils/5._vbscript_callback`: PopperSol
- `games/tran.json#/coils/5._inferred_type`: ball_management
- `games/tran.json#/coils/5._note`: Kicks ball from sw15 saucer
- `games/tran.json#/coils/6._vbscript_callback`: SolKnocker
- `games/tran.json#/coils/6._inferred_type`: knocker
- `games/tran.json#/coils/7._vbscript_callback`: RightLockSol
- `games/tran.json#/coils/7._inferred_type`: ball_management
- `games/tran.json#/coils/7._note`: Fires LockRSol kicker
- `games/tran.json#/coils/8._vbscript_callback`: SolGI
- `games/tran.json#/coils/8._inferred_type`: gi_relay
- `games/tran.json#/coils/8._note`: Inverted logic — Enabled=true turns GI OFF, Enabled=false turns GI ON
- `games/tran.json#/coils/9._vbscript_callback`: GateOpen
- `games/tran.json#/coils/9._inferred_type`: gate
- `games/tran.json#/coils/9._note`: Controls GateSol10 open/close
- `games/tran.json#/coils/10._vbscript_callback`: Turn1Flash
- `games/tran.json#/coils/10._inferred_type`: flasher
- `games/tran.json#/coils/11._vbscript_callback`: AutoFireSol
- `games/tran.json#/coils/11._inferred_type`: ball_management
- `games/tran.json#/coils/11._note`: Fires Kickback kicker
- `games/tran.json#/coils/12._vbscript_callback`: Turn2Flash
- `games/tran.json#/coils/12._inferred_type`: flasher
- `games/tran.json#/coils/13._vbscript_callback`: Turn3Flash
- `games/tran.json#/coils/13._inferred_type`: flasher
- `games/tran.json#/coils/13._note`: Controls Turn3Flasher VPX object
- `games/tran.json#/coils/14._vbscript_callback`: PF2XFlash
- `games/tran.json#/coils/14._inferred_type`: flasher
- `games/tran.json#/coils/14._note`: Controls PF2XFlasher VPX object
- `games/tran.json#/coils/15._vbscript_callback`: BridgeFlash
- `games/tran.json#/coils/15._inferred_type`: flasher
- `games/tran.json#/coils/15._note`: Controls BridgeFlasher VPX object
- `games/tran.json#/coils/16._vbscript_callback`: TopLeftFlash
- `games/tran.json#/coils/16._inferred_type`: flasher
- `games/tran.json#/coils/16._note`: Triggers FlasherFlash1 and FlasherFlash2
- `games/tran.json#/coils/17._vbscript_callback`: JetFlash
- `games/tran.json#/coils/17._inferred_type`: flasher
- `games/tran.json#/coils/17._note`: Triggers FlasherFlash3 and FlasherFlash4
- `games/tran.json#/coils/18._vbscript_callback`: BallLockFlash
- `games/tran.json#/coils/18._inferred_type`: flasher
- `games/tran.json#/coils/18._note`: Controls BallLockFlasher with fade effect
- `games/tran.json#/coils/19._vbscript_callback`: SingleStandupFlash
- `games/tran.json#/coils/19._inferred_type`: flasher
- `games/tran.json#/coils/19._note`: Controls SingleSUFlasher VPX object
- `games/tran.json#/coils/20._vbscript_callback`: BallPopperFlash
- `games/tran.json#/coils/20._inferred_type`: flasher
- `games/tran.json#/coils/20._note`: Routes through Lampz.state(107) with fade
- `games/tran.json#/coils/21._vbscript_callback`: PF3XFlash
- `games/tran.json#/coils/21._inferred_type`: flasher
- `games/tran.json#/coils/21._note`: Controls PF3XFlasher VPX object
- `games/tran.json#/coils/22._vbscript_callback`: SolURFlipper
- `games/tran.json#/coils/22._inferred_type`: flipper
- `games/tran.json#/coils/22._note`: Framework constant sURFlipper from S11.VBS
- `games/tran.json#/coils/23._vbscript_callback`: SolRFlipper
- `games/tran.json#/coils/23._inferred_type`: flipper
- `games/tran.json#/coils/23._note`: Framework constant sLRFlipper from core.vbs
- `games/tran.json#/coils/24._vbscript_callback`: SolLFlipper
- `games/tran.json#/coils/24._inferred_type`: flipper
- `games/tran.json#/coils/24._note`: Framework constant sLLFlipper from core.vbs
- `games/tran.json#/lamps/39._note`: Non-matrix lamp — driven via SetLamp(107) from BallPopperFlash coil 31. VPX objects: BallPopperFlasher, BallPopperFlasherb, BallPopperFlasherc
- `games/tran.json#/lamps/40._note`: Non-matrix lamp — controlled by SolGI (coil 9). Lampz.state(109) tracks GI on/off state
- `games/tran.json#/_source/confidence_notes`: High confidence on switches/coils from SolCallback and Controller.Switch handlers. Uses S11.VBS (System 11). Custom 'realish trough' with 3 balls — no cvpmTrough/cvpmBallStack used, trough is manually coded with switches 10-13. Flasher coils (11, 15-16, 25-32) use various flash sub implementations. Lamps extracted from Lampz.MassAssign block. Commented-out SolCallbacks 17-21 were bumper/slingshot sound-only callbacks, not physical coils — omitted. swTilt and sURFlipper are S11.VBS framework constants (swTilt=57, sURFlipper=34). Manufacturer listed as Bally in script splash line (Bally/Midway merger era). Drop target switches (19-24) use custom DTHit handler with TargetBouncer animation.

## Unresolved questions

- Is the I/O enumeration complete for every supported physical/controller variant?
- Which inferred VPX behaviors reflect real hardware, and which are table-script conveniences?
- Are all mechanism home states, sensors, motion constraints, and ball interactions documented?

## Sources

- `legacy.game.tran`: `games/tran.json` at the pinned migration revision.
