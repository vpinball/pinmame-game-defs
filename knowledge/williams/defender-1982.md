# Defender

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

- `games/defender.json#/switches/4._inferred_type`: drop_target
- `games/defender.json#/switches/4._note`: 5-target left bank (sw13-17), reset individually by coils 1-5 or bank-dropped by coil 6
- `games/defender.json#/switches/5._inferred_type`: drop_target
- `games/defender.json#/switches/6._inferred_type`: drop_target
- `games/defender.json#/switches/7._inferred_type`: drop_target
- `games/defender.json#/switches/8._inferred_type`: drop_target
- `games/defender.json#/switches/9._inferred_type`: standup_target
- `games/defender.json#/switches/10._inferred_type`: standup_target
- `games/defender.json#/switches/11._inferred_type`: standup_target
- `games/defender.json#/switches/12._inferred_type`: standup_target
- `games/defender.json#/switches/13._inferred_type`: standup_target
- `games/defender.json#/switches/14._inferred_type`: drop_target
- `games/defender.json#/switches/14._note`: 5-target right bank (sw23-27), reset individually by coils 33-37 or bank-dropped by coil 38 (multiplexed via sol 11)
- `games/defender.json#/switches/15._inferred_type`: drop_target
- `games/defender.json#/switches/16._inferred_type`: drop_target
- `games/defender.json#/switches/17._inferred_type`: drop_target
- `games/defender.json#/switches/18._inferred_type`: drop_target
- `games/defender.json#/switches/19._inferred_type`: standup_target
- `games/defender.json#/switches/20._inferred_type`: standup_target
- `games/defender.json#/switches/21._inferred_type`: standup_target
- `games/defender.json#/switches/22._inferred_type`: standup_target
- `games/defender.json#/switches/23._inferred_type`: standup_target
- `games/defender.json#/switches/24._inferred_type`: drop_target
- `games/defender.json#/switches/24._note`: 3-target center bank (sw33-35), reset individually by coils 9/41/10 or bank-dropped by coil 42
- `games/defender.json#/switches/25._inferred_type`: drop_target
- `games/defender.json#/switches/26._inferred_type`: drop_target
- `games/defender.json#/switches/27._inferred_type`: standup_target
- `games/defender.json#/switches/28._inferred_type`: standup_target
- `games/defender.json#/switches/29._inferred_type`: rubber
- `games/defender.json#/switches/29._note`: Pulsed via vpmTimer.pulseSw 38
- `games/defender.json#/switches/30._inferred_type`: drop_target
- `games/defender.json#/switches/30._note`: Single drop target, reset by coil 7
- `games/defender.json#/switches/31._inferred_type`: drop_target
- `games/defender.json#/switches/31._note`: Single drop target, reset by coil 39 (multiplexed via sol 11)
- `games/defender.json#/switches/32._inferred_type`: standup_target
- `games/defender.json#/switches/33._inferred_type`: ball_lock
- `games/defender.json#/switches/33._note`: 3-ball lock (sw42-44). Balls stack via UpdateLock cascade. Released by coil 40.
- `games/defender.json#/switches/34._inferred_type`: ball_lock
- `games/defender.json#/switches/35._inferred_type`: ball_lock
- `games/defender.json#/switches/35._note`: Top of lock stack — SoundSaucerLock on hit
- `games/defender.json#/switches/38._note`: 3-ball trough (sw47-49). Balls cascade via UpdateTrough timer. Ball release from sw47.
- `games/defender.json#/switches/41._note`: Also sets BIPL flag on hit (Ball In Play Latch)
- `games/defender.json#/switches/46._inferred_type`: bumper
- `games/defender.json#/switches/46._note`: Bumper1 — pulsed via vpmTimer.PulseSw(55)
- `games/defender.json#/switches/47._inferred_type`: bumper
- `games/defender.json#/switches/47._note`: Bumper2 — pulsed via vpmTimer.PulseSw(56)
- `games/defender.json#/switches/48._inferred_type`: slingshot
- `games/defender.json#/switches/48._note`: Pulsed via vpmTimer.PulseSw 57
- `games/defender.json#/switches/49._inferred_type`: slingshot
- `games/defender.json#/switches/49._note`: Pulsed via vpmTimer.PulseSw 58
- `games/defender.json#/switches/50._note`: Mapped to RightMagnaSave and LockBarKey keypresses
- `games/defender.json#/switches/51._note`: Mapped to LeftMagnaSave keypress
- `games/defender.json#/coils/0._vbscript_callback`: SolDTLBankUnhit 13,
- `games/defender.json#/coils/0._inferred_type`: drop_target_reset
- `games/defender.json#/coils/0._note`: Resets individual target sw13
- `games/defender.json#/coils/1._vbscript_callback`: SolDTLBankUnhit 14,
- `games/defender.json#/coils/1._inferred_type`: drop_target_reset
- `games/defender.json#/coils/1._note`: Resets individual target sw14
- `games/defender.json#/coils/2._vbscript_callback`: SolDTLBankUnhit 15,
- `games/defender.json#/coils/2._inferred_type`: drop_target_reset
- `games/defender.json#/coils/2._note`: Resets individual target sw15
- `games/defender.json#/coils/3._vbscript_callback`: SolDTLBankUnhit 16,
- `games/defender.json#/coils/3._inferred_type`: drop_target_reset
- `games/defender.json#/coils/3._note`: Resets individual target sw16
- `games/defender.json#/coils/4._vbscript_callback`: SolDTLBankUnhit 17,
- `games/defender.json#/coils/4._inferred_type`: drop_target_reset
- `games/defender.json#/coils/4._note`: Resets individual target sw17
- `games/defender.json#/coils/5._vbscript_callback`: SolDTLBankDropDown
- `games/defender.json#/coils/5._inferred_type`: drop_target_reset
- `games/defender.json#/coils/5._note`: Drops all left bank targets (sw13-17)
- `games/defender.json#/coils/6._vbscript_callback`: SolDTBPodDropUp
- `games/defender.json#/coils/6._inferred_type`: drop_target_reset
- `games/defender.json#/coils/6._note`: Raises sw39
- `games/defender.json#/coils/7._vbscript_callback`: SolRelease
- `games/defender.json#/coils/7._inferred_type`: ball_management
- `games/defender.json#/coils/7._note`: Kicks ball from sw47 (trough position 1)
- `games/defender.json#/coils/8._vbscript_callback`: SolDTBait1
- `games/defender.json#/coils/8._inferred_type`: drop_target_reset
- `games/defender.json#/coils/8._note`: Raises sw33
- `games/defender.json#/coils/9._vbscript_callback`: SolDTBait3
- `games/defender.json#/coils/9._inferred_type`: drop_target_reset
- `games/defender.json#/coils/9._note`: Raises sw35
- `games/defender.json#/coils/10._vbscript_callback`: SolDrain
- `games/defender.json#/coils/10._inferred_type`: ball_management
- `games/defender.json#/coils/10._note`: Kicks ball from sw46 (outhole) into trough
- `games/defender.json#/coils/11._vbscript_callback`: SolAPlunger
- `games/defender.json#/coils/11._inferred_type`: ball_management
- `games/defender.json#/coils/11._note`: Fires Plunger1 to launch ball; pulls back on disable
- `games/defender.json#/coils/12._vbscript_callback`: SolPFGI
- `games/defender.json#/coils/12._inferred_type`: gi_relay
- `games/defender.json#/coils/12._note`: Enabled = GI off (Lampz.state(0)=0, dark backglass), Disabled = GI on (Lampz.state(0)=1, illuminated backglass)
- `games/defender.json#/coils/13._vbscript_callback`: SolKnocker
- `games/defender.json#/coils/13._inferred_type`: knocker
- `games/defender.json#/coils/14._inferred_type`: bumper
- `games/defender.json#/coils/14._note`: SolCallback commented out in script
- `games/defender.json#/coils/15._inferred_type`: bumper
- `games/defender.json#/coils/15._note`: SolCallback commented out in script
- `games/defender.json#/coils/16._vbscript_callback`: SolCenterFlasher
- `games/defender.json#/coils/16._inferred_type`: flasher
- `games/defender.json#/coils/16._note`: Controls Lampz.state(100) — mapped to flash1/flash2/flash3/flash4/flashh VPX objects
- `games/defender.json#/coils/17._vbscript_callback`: SolFlipperDiverter
- `games/defender.json#/coils/17._inferred_type`: diverter
- `games/defender.json#/coils/17._note`: Uses Flipper3 RotateToEnd/RotateToStart for diverter motion
- `games/defender.json#/coils/18._vbscript_callback`: SolRun
- `games/defender.json#/coils/18._inferred_type`: game_on
- `games/defender.json#/coils/18._note`: Enables flippers and slingshots; disables on game end
- `games/defender.json#/coils/19._vbscript_callback`: SolDTRBankUnhit 23,
- `games/defender.json#/coils/19._inferred_type`: drop_target_reset
- `games/defender.json#/coils/19._note`: Multiplexed via sol 11. Resets individual target sw23
- `games/defender.json#/coils/20._vbscript_callback`: SolDTRBankUnhit 24,
- `games/defender.json#/coils/20._inferred_type`: drop_target_reset
- `games/defender.json#/coils/20._note`: Multiplexed via sol 11. Resets individual target sw24
- `games/defender.json#/coils/21._vbscript_callback`: SolDTRBankUnhit 25,
- `games/defender.json#/coils/21._inferred_type`: drop_target_reset
- `games/defender.json#/coils/21._note`: Multiplexed via sol 11. Resets individual target sw25
- `games/defender.json#/coils/22._vbscript_callback`: SolDTRBankUnhit 26,
- `games/defender.json#/coils/22._inferred_type`: drop_target_reset
- `games/defender.json#/coils/22._note`: Multiplexed via sol 11. Resets individual target sw26
- `games/defender.json#/coils/23._vbscript_callback`: SolDTRBankUnhit 27,
- `games/defender.json#/coils/23._inferred_type`: drop_target_reset
- `games/defender.json#/coils/23._note`: Multiplexed via sol 11. Resets individual target sw27
- `games/defender.json#/coils/24._vbscript_callback`: SolDTRBankDropDown
- `games/defender.json#/coils/24._inferred_type`: drop_target_reset
- `games/defender.json#/coils/24._note`: Multiplexed via sol 11. Drops all right bank targets (sw23-27)
- `games/defender.json#/coils/25._vbscript_callback`: SolDTTPodDropUp
- `games/defender.json#/coils/25._inferred_type`: drop_target_reset
- `games/defender.json#/coils/25._note`: Multiplexed via sol 11. Raises sw40
- `games/defender.json#/coils/26._vbscript_callback`: SolUnlock
- `games/defender.json#/coils/26._inferred_type`: ball_management
- `games/defender.json#/coils/26._note`: Multiplexed via sol 11. Kicks ball from sw42 (lock position 1)
- `games/defender.json#/coils/27._vbscript_callback`: SolDTBait2
- `games/defender.json#/coils/27._inferred_type`: drop_target_reset
- `games/defender.json#/coils/27._note`: Multiplexed via sol 11. Raises sw34
- `games/defender.json#/coils/28._vbscript_callback`: SolDTBaitDropDown
- `games/defender.json#/coils/28._inferred_type`: drop_target_reset
- `games/defender.json#/coils/28._note`: Multiplexed via sol 11. Drops all center targets (sw33-35)
- `games/defender.json#/coils/29._note`: SolCallback blanked for fast-flip workaround. Flipper driven directly via KeyDown/KeyUp calling SolRFlipper. Framework constant from S7.VBS.
- `games/defender.json#/coils/30._note`: SolCallback blanked for fast-flip workaround. Flipper driven directly via KeyDown/KeyUp calling SolLFlipper. Also drives LeftFlipper1 (upper left). Framework constant from S7.VBS.
- `games/defender.json#/lamps/0._note`: Solenoid-driven via SolPFGI (coil 14). Lampz.state(0) set by coil callback, not lamp matrix. Controls GI light collection.
- `games/defender.json#/lamps/1._note`: Status lamp — Controller.Lamp(1) used in UpdateMultipleLamps (VR: l1, Desktop: ShootAgainReel)
- `games/defender.json#/lamps/2._note`: Status lamp — Controller.Lamp(2)
- `games/defender.json#/lamps/3._note`: Status lamp — Controller.Lamp(3)
- `games/defender.json#/lamps/4._note`: Status lamp — Controller.Lamp(4)
- `games/defender.json#/lamps/5._note`: Status lamp — Controller.Lamp(5)
- `games/defender.json#/lamps/6._note`: Status lamp — Controller.Lamp(6), dual VPX objects l6/l6a
- `games/defender.json#/lamps/7._note`: Playfield insert — Lampz.MassAssign(7)
- `games/defender.json#/lamps/8._note`: Status lamp — Controller.Lamp(8)
- `games/defender.json#/lamps/9._note`: Lampz.MassAssign(9) with Light9h highlight prim
- `games/defender.json#/lamps/39._note`: Also has Light39f flasher variant
- `games/defender.json#/lamps/40._note`: Also has Light40f flasher variant
- `games/defender.json#/lamps/41._note`: Also has Light41f flasher variant
- `games/defender.json#/lamps/42._note`: Also has Light42f flasher variant
- `games/defender.json#/lamps/55._note`: Also has Light55f flasher variant
- `games/defender.json#/lamps/56._note`: Also has Light56f flasher variant
- `games/defender.json#/lamps/63._note`: Solenoid-driven via SolCenterFlasher (coil 21). Lampz.state(100) set by coil callback. Mapped to flash1/flash2/flash3/flash4/flashh VPX objects.
- `games/defender.json#/_source/confidence_notes`: High confidence on switches/coils from SolCallback and sw*_Hit handlers. Lamp assignments from InitLampsNF Lampz.MassAssign and Controller.Lamp comments in UpdateMultipleLamps/UpdateDTLamps. Uses S7.VBS (Williams System 7). Solenoid 11 is multiplexed per System 7 convention — coils 33-42 are multiplexed via sol 11 (VPM 1.52+ handles automatically, older versions offset by +32). Lamp 0 is GI (solenoid-driven via SolPFGI on coil 14). Lamp 100 is center flasher (solenoid-driven via SolCenterFlasher on coil 21). Tilt switch is swTilt from S7.VBS framework (platform-defined, typically switch 2 on System 7). Flipper solenoid callbacks are blanked for fast-flip workaround — flippers are driven directly in KeyDown/KeyUp subs.

## Unresolved questions

- Is the I/O enumeration complete for every supported physical/controller variant?
- Which inferred VPX behaviors reflect real hardware, and which are table-script conveniences?
- Are all mechanism home states, sensors, motion constraints, and ball interactions documented?

## Sources

- `legacy.game.defender`: `games/defender.json` at the pinned migration revision.
