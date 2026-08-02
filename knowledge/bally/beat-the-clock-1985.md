# Beat The Clock

Coverage: **partial - source-derived recreation knowledge requiring validation**

## Overview

Legacy evidence identifies this candidate as Bally (1985). The information below is preserved for recreation work but is not automatically treated as validated physical-machine fact.

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
- `games/btc.json#/switches/0._inferred_type`: drop_target
- `games/btc.json#/switches/0._note`: DTHit 1 — part of 1-6 bank, reset by sol 11
- `games/btc.json#/switches/1._inferred_type`: drop_target
- `games/btc.json#/switches/1._note`: DTHit 2 — part of 1-6 bank, reset by sol 11
- `games/btc.json#/switches/2._inferred_type`: drop_target
- `games/btc.json#/switches/2._note`: DTHit 3 — part of 1-6 bank, reset by sol 11
- `games/btc.json#/switches/3._inferred_type`: drop_target
- `games/btc.json#/switches/3._note`: DTHit 4 — part of 1-6 bank, reset by sol 11
- `games/btc.json#/switches/4._inferred_type`: drop_target
- `games/btc.json#/switches/4._note`: DTHit 5 — part of 1-6 bank, reset by sol 11
- `games/btc.json#/switches/5._inferred_type`: drop_target
- `games/btc.json#/switches/5._note`: DTHit 7 — part of 1-6 bank, reset by sol 11. Bank is sw1-5,7 (no sw6)
- `games/btc.json#/switches/6._inferred_type`: trough
- `games/btc.json#/switches/6._note`: Physical trough, single ball. Initialized in Table1_Init with Controller.Switch(8)=1
- `games/btc.json#/switches/7._note`: Mapped to RightFlipperKey in KeyDown/KeyUp
- `games/btc.json#/switches/8._inferred_type`: trigger
- `games/btc.json#/switches/9._note`: vpmNudge.TiltSwitch=15
- `games/btc.json#/switches/10._inferred_type`: trigger
- `games/btc.json#/switches/11._inferred_type`: standup_target
- `games/btc.json#/switches/11._note`: STHit 17 — pulsed via Roth ST system
- `games/btc.json#/switches/12._inferred_type`: standup_target
- `games/btc.json#/switches/12._note`: STHit 18
- `games/btc.json#/switches/13._inferred_type`: standup_target
- `games/btc.json#/switches/13._note`: STHit 19
- `games/btc.json#/switches/14._inferred_type`: standup_target
- `games/btc.json#/switches/14._note`: STHit 20
- `games/btc.json#/switches/15._inferred_type`: standup_target
- `games/btc.json#/switches/15._note`: STHit 21
- `games/btc.json#/switches/16._inferred_type`: trigger
- `games/btc.json#/switches/17._inferred_type`: trigger
- `games/btc.json#/switches/18._inferred_type`: bumper
- `games/btc.json#/switches/18._note`: Bumper1 — pulsed via vpmTimer.PulseSw 25
- `games/btc.json#/switches/19._inferred_type`: bumper
- `games/btc.json#/switches/19._note`: Bumper2 — pulsed via vpmTimer.PulseSw 26
- `games/btc.json#/switches/20._inferred_type`: bumper
- `games/btc.json#/switches/20._note`: Bumper3 — pulsed via vpmTimer.PulseSw 27
- `games/btc.json#/switches/21._inferred_type`: slingshot
- `games/btc.json#/switches/21._note`: Pulsed via vpmTimer.PulseSw 28
- `games/btc.json#/switches/22._inferred_type`: slingshot
- `games/btc.json#/switches/22._note`: Pulsed via vpmTimer.PulseSw 29
- `games/btc.json#/switches/23._inferred_type`: trigger
- `games/btc.json#/switches/24._inferred_type`: trigger
- `games/btc.json#/switches/25._inferred_type`: trigger
- `games/btc.json#/switches/25._note`: Also toggles L16 lamp state on hit/timer
- `games/btc.json#/switches/26._inferred_type`: standup_target
- `games/btc.json#/switches/26._note`: STHit 33
- `games/btc.json#/switches/27._inferred_type`: standup_target
- `games/btc.json#/switches/27._note`: STHit 34
- `games/btc.json#/switches/28._inferred_type`: standup_target
- `games/btc.json#/switches/28._note`: STHit 35
- `games/btc.json#/switches/29._inferred_type`: standup_target
- `games/btc.json#/switches/29._note`: STHit 36
- `games/btc.json#/switches/30._inferred_type`: trigger
- `games/btc.json#/switches/31._inferred_type`: trigger
- `games/btc.json#/switches/32._inferred_type`: trigger
- `games/btc.json#/switches/33._inferred_type`: trigger
- `games/btc.json#/switches/34._inferred_type`: drop_target
- `games/btc.json#/switches/34._note`: DTHit 45 — standalone target, reset by sol 10
- `games/btc.json#/switches/35._inferred_type`: kicker
- `games/btc.json#/switches/35._note`: Kicked by sol 8 (SolOut46)
- `games/btc.json#/switches/36._inferred_type`: kicker
- `games/btc.json#/switches/36._note`: Kicked by sol 9 (SolOut47)
- `games/btc.json#/coils/0._vbscript_callback`: Flasher6
- `games/btc.json#/coils/0._inferred_type`: flasher
- `games/btc.json#/coils/0._note`: Controls 4 sub-flashers: F6a, F6b, F6c, F6d
- `games/btc.json#/coils/1._vbscript_callback`: Flasher7
- `games/btc.json#/coils/1._inferred_type`: flasher
- `games/btc.json#/coils/1._note`: No-op in script (empty sub)
- `games/btc.json#/coils/2._vbscript_callback`: SolOut46
- `games/btc.json#/coils/2._inferred_type`: kicker
- `games/btc.json#/coils/2._note`: Kicks ball from sw46
- `games/btc.json#/coils/3._vbscript_callback`: SolOut47
- `games/btc.json#/coils/3._inferred_type`: kicker
- `games/btc.json#/coils/3._note`: Kicks ball from sw47
- `games/btc.json#/coils/4._vbscript_callback`: SolDropUpDTR
- `games/btc.json#/coils/4._inferred_type`: drop_target_reset
- `games/btc.json#/coils/4._note`: Raises sw45
- `games/btc.json#/coils/5._vbscript_callback`: SolDropUpDTL
- `games/btc.json#/coils/5._inferred_type`: drop_target_reset
- `games/btc.json#/coils/5._note`: Raises sw1-5,7 (full left bank)
- `games/btc.json#/coils/6._vbscript_callback`: SolRelease
- `games/btc.json#/coils/6._inferred_type`: ball_management
- `games/btc.json#/coils/6._note`: Releases ball from sw8 trough
- `games/btc.json#/coils/7._vbscript_callback`: vpmSolSound SoundFX("Knocker_1",DOFKnocker),
- `games/btc.json#/coils/7._inferred_type`: knocker
- `games/btc.json#/coils/8._vbscript_callback`: SolGIOn
- `games/btc.json#/coils/8._inferred_type`: gi_relay
- `games/btc.json#/coils/8._note`: Controls playfield general illumination via SetGI
- `games/btc.json#/_source/confidence_notes`: High confidence on switches/coils from SolCallback and sw*_Hit handlers. Uses BALLY.VBS platform. Physical trough with single ball (sw8). Lamps extracted from VLM BL_L_l## arrays (light numbers correspond to ROM lamp outputs via vpmMapLights AllLamps with TimerInterval). Flashers driven via solenoid 6 (4 sub-flashers F6a-F6d) and solenoid 7 (no-op in script). GI controlled by solenoid 17 via SetGI. Drop targets use Roth DT system (DTHit/DTRaise). Standup targets use Roth ST system (STHit with PulseSw). ROM beatclc2 has flasher support; beatclck is alternate without.

## Unresolved questions

- Is the I/O enumeration complete for every supported physical/controller variant?
- Which inferred VPX behaviors reflect real hardware, and which are table-script conveniences?
- Are all mechanism home states, sensors, motion constraints, and ball interactions documented?

## Sources

- `legacy.game.btc`: `games/btc.json` at the pinned migration revision.
