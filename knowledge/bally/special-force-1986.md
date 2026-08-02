# Special Force

Coverage: **partial - source-derived recreation knowledge requiring validation**

## Overview

Legacy evidence identifies this candidate as Bally (1986). The information below is preserved for recreation work but is not automatically treated as validated physical-machine fact.

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
- `games/specfor.json#/switches/0._inferred_type`: target
- `games/specfor.json#/switches/0._note`: Pulsed via vpmTimer.PulseSw 1
- `games/specfor.json#/switches/1._inferred_type`: target
- `games/specfor.json#/switches/1._note`: Pulsed via vpmTimer.PulseSw 2
- `games/specfor.json#/switches/2._inferred_type`: target
- `games/specfor.json#/switches/2._note`: Pulsed via vpmTimer.PulseSw 3. Also triggers wire ramp on/off based on ball direction.
- `games/specfor.json#/switches/3._inferred_type`: rubber
- `games/specfor.json#/switches/3._note`: Pulsed via vpmTimer.PulseSw 4 from sw4Rubber1-5_Hit
- `games/specfor.json#/switches/4._note`: Activated by LeftMagnaSave key
- `games/specfor.json#/switches/5._note`: Activated by RightMagnaSave key
- `games/specfor.json#/switches/6._note`: Drain switch — ball enters here, kicked to trough by SolDrain (Mult14 when L3=1)
- `games/specfor.json#/switches/7._inferred_type`: rollover
- `games/specfor.json#/switches/8._inferred_type`: rollover
- `games/specfor.json#/switches/9._inferred_type`: standup_target
- `games/specfor.json#/switches/9._note`: Hit via STHit 16
- `games/specfor.json#/switches/10._inferred_type`: standup_target
- `games/specfor.json#/switches/10._note`: Hit via STHit 17
- `games/specfor.json#/switches/11._inferred_type`: standup_target
- `games/specfor.json#/switches/11._note`: Hit via STHit 18
- `games/specfor.json#/switches/12._inferred_type`: standup_target
- `games/specfor.json#/switches/12._note`: Hit via STHit 19
- `games/specfor.json#/switches/13._inferred_type`: standup_target
- `games/specfor.json#/switches/13._note`: Hit via STHit 20
- `games/specfor.json#/switches/14._inferred_type`: standup_target
- `games/specfor.json#/switches/14._note`: Hit via STHit 21
- `games/specfor.json#/switches/15._inferred_type`: standup_target
- `games/specfor.json#/switches/15._note`: Hit via STHit 22
- `games/specfor.json#/switches/16._inferred_type`: kicker
- `games/specfor.json#/switches/16._note`: Ball locks in saucer. Kicked out by Mult10 (sol 10) when L3=1.
- `games/specfor.json#/switches/17._inferred_type`: rollover
- `games/specfor.json#/switches/18._inferred_type`: bumper
- `games/specfor.json#/switches/18._note`: Bumper1 — pulsed via vpmTimer.PulseSw(25)
- `games/specfor.json#/switches/19._inferred_type`: bumper
- `games/specfor.json#/switches/19._note`: Bumper2 — pulsed via vpmTimer.PulseSw(26)
- `games/specfor.json#/switches/20._inferred_type`: bumper
- `games/specfor.json#/switches/20._note`: Bumper3 — pulsed via vpmTimer.PulseSw(27)
- `games/specfor.json#/switches/24._inferred_type`: standup_target
- `games/specfor.json#/switches/24._note`: Hit via STHit 33
- `games/specfor.json#/switches/25._inferred_type`: standup_target
- `games/specfor.json#/switches/25._note`: Hit via STHit 34
- `games/specfor.json#/switches/26._inferred_type`: standup_target
- `games/specfor.json#/switches/26._note`: Hit via STHit 35
- `games/specfor.json#/switches/27._inferred_type`: standup_target
- `games/specfor.json#/switches/27._note`: Hit via STHit 36
- `games/specfor.json#/switches/28._inferred_type`: drop_target
- `games/specfor.json#/switches/28._note`: Hit via DTHit 38. Reset by Mult14 (sol 14) when L3=1.
- `games/specfor.json#/switches/29._inferred_type`: drop_target
- `games/specfor.json#/switches/29._note`: Hit via DTHit 40. Reset by sol 11 (DTRaise40), dropped by sol 12 (DTDrop40).
- `games/specfor.json#/switches/30._inferred_type`: rollover
- `games/specfor.json#/switches/31._inferred_type`: rollover
- `games/specfor.json#/switches/31._note`: Two VPX triggers (sw42a, sw42b) both map to ROM switch 42. Ball velocity dampened on exit.
- `games/specfor.json#/switches/32._inferred_type`: standup_target
- `games/specfor.json#/switches/32._note`: Hit via STHit 43
- `games/specfor.json#/switches/33._inferred_type`: standup_target
- `games/specfor.json#/switches/33._note`: Hit via STHit 44 with TargetBouncer applied
- `games/specfor.json#/switches/34._inferred_type`: drop_target
- `games/specfor.json#/switches/34._note`: Hit via DTHit 45. Part of 3-target inline bank (sw45-47). Reset by Mult6 (sol 6) when L3=1.
- `games/specfor.json#/switches/35._inferred_type`: drop_target
- `games/specfor.json#/switches/35._note`: Hit via DTHit 46. Part of 3-target inline bank (sw45-47). Reset by Mult6 (sol 6) when L3=1.
- `games/specfor.json#/switches/36._inferred_type`: drop_target
- `games/specfor.json#/switches/36._note`: Hit via DTHit 47. Part of 3-target inline bank (sw45-47). Reset by Mult6 (sol 6) when L3=1.
- `games/specfor.json#/switches/37._inferred_type`: target
- `games/specfor.json#/switches/37._note`: Pulsed via vpmTimer.PulseSw 48
- `games/specfor.json#/coils/0._vbscript_callback`: SolLBumper
- `games/specfor.json#/coils/0._inferred_type`: bumper
- `games/specfor.json#/coils/0._note`: Fires Bumper1
- `games/specfor.json#/coils/1._vbscript_callback`: SolRBumper
- `games/specfor.json#/coils/1._inferred_type`: bumper
- `games/specfor.json#/coils/1._note`: Fires Bumper2
- `games/specfor.json#/coils/2._vbscript_callback`: SolMBumper
- `games/specfor.json#/coils/2._inferred_type`: bumper
- `games/specfor.json#/coils/2._note`: Fires Bumper3
- `games/specfor.json#/coils/3._vbscript_callback`: Mult6
- `games/specfor.json#/coils/3._inferred_type`: multiplexed
- `games/specfor.json#/coils/3._note`: When L3=1: resets inline drop targets sw45-47. When L3=0: controls bright lights group 101. Bally -35 multiplexed solenoid.
- `games/specfor.json#/coils/4._vbscript_callback`: Mult7
- `games/specfor.json#/coils/4._inferred_type`: multiplexed
- `games/specfor.json#/coils/4._note`: When L3=1: drops sw45 (bottom inline target). When L3=0: controls bright lights group 102.
- `games/specfor.json#/coils/5._vbscript_callback`: Mult8
- `games/specfor.json#/coils/5._inferred_type`: multiplexed
- `games/specfor.json#/coils/5._note`: When L3=1: drops sw46 (middle inline target). When L3=0: controls bright lights group 103.
- `games/specfor.json#/coils/6._vbscript_callback`: Mult9
- `games/specfor.json#/coils/6._inferred_type`: multiplexed
- `games/specfor.json#/coils/6._note`: When L3=1: drops sw47 (top inline target). When L3=0: controls bright lights group 104.
- `games/specfor.json#/coils/7._vbscript_callback`: Mult10
- `games/specfor.json#/coils/7._inferred_type`: multiplexed
- `games/specfor.json#/coils/7._note`: When L3=1: kicks ball from saucer (sw23). When L3=0: controls bright lights group 105.
- `games/specfor.json#/coils/8._vbscript_callback`: DTRaise40
- `games/specfor.json#/coils/8._inferred_type`: drop_target_reset
- `games/specfor.json#/coils/8._note`: Raises drop target sw40
- `games/specfor.json#/coils/9._vbscript_callback`: DTDrop40
- `games/specfor.json#/coils/9._inferred_type`: drop_target_drop
- `games/specfor.json#/coils/9._note`: Drops drop target sw40
- `games/specfor.json#/coils/10._vbscript_callback`: Mult14
- `games/specfor.json#/coils/10._inferred_type`: multiplexed
- `games/specfor.json#/coils/10._note`: When L3=1: resets single capture drop target sw38. When L3=0: SolDrain — kicks ball from outhole (sw8) to trough.
- `games/specfor.json#/coils/11._vbscript_callback`: Mult15
- `games/specfor.json#/coils/11._inferred_type`: multiplexed
- `games/specfor.json#/coils/11._note`: When L3=1: SolRelease — releases ball from trough (sw30). When L3=0: fires knocker solenoid.
- `games/specfor.json#/coils/12._vbscript_callback`: SolGameOn
- `games/specfor.json#/coils/12._inferred_type`: game_on
- `games/specfor.json#/coils/13._note`: SolCallback assigned to empty string
- `games/specfor.json#/lamps/72._note`: GI string — controlled via LM_GI_l60a
- `games/specfor.json#/lamps/73._note`: GI string — controlled via LM_GI_l61a
- `games/specfor.json#/lamps/74._note`: GI string — controlled via LM_GI_l62a
- `games/specfor.json#/lamps/75._note`: GI string — controlled via LM_GI_l63a
- `games/specfor.json#/lamps/76._note`: GI string — controlled via LM_GI_l76a
- `games/specfor.json#/lamps/77._note`: GI string — controlled via LM_GI_l77a
- `games/specfor.json#/lamps/78._note`: GI string — controlled via LM_GI_l78
- `games/specfor.json#/lamps/79._note`: GI string — controlled via LM_GI_l79a
- `games/specfor.json#/lamps/80._note`: GI string — controlled via LM_GI_l91a
- `games/specfor.json#/lamps/81._note`: GI string — controlled via LM_GI_l92a
- `games/specfor.json#/lamps/82._note`: GI string — controlled via LM_GI_l93a
- `games/specfor.json#/lamps/83._note`: GI string — controlled via LM_GI_l94a
- `games/specfor.json#/lamps/84._note`: GI string — controlled via LM_GI_l100a through l100d. Represents 4 GI zones across playfield.
- `games/specfor.json#/lamps/85._note`: Solenoid-driven via Mult6 (sol 6) when L3=0. BRL group controlled by ManualLightsUpdate.
- `games/specfor.json#/lamps/86._note`: Solenoid-driven via Mult7 (sol 7) when L3=0. BRL group controlled by ManualLightsUpdate.
- `games/specfor.json#/lamps/87._note`: Solenoid-driven via Mult8 (sol 8) when L3=0. BRL group controlled by ManualLightsUpdate.
- `games/specfor.json#/lamps/88._note`: Solenoid-driven via Mult9 (sol 9) when L3=0. BRL group controlled by ManualLightsUpdate.
- `games/specfor.json#/lamps/89._note`: Solenoid-driven via Mult10 (sol 10) when L3=0. BRL group controlled by ManualLightsUpdate.
- `games/specfor.json#/_source/confidence_notes`: High confidence on switches/coils from SolCallback and sw*_Hit handlers. Uses 6803.VBS (Bally 6803 MPU). Solenoids 6-10, 14-15 are multiplexed: when L3 is lit they control drop targets/kicker/ball management, when L3 is off they control bright light relays (lamps 101-105) or knocker/outhole. swTilt is a framework constant from 6803.VBS (typically sw14 on Bally -35/6803). Lamp numbers extracted from VLM baked lighting arrays (LM_Inserts_l##). GI lamps (60-63, 76-79, 91-94, 100a-d) and BRL lamps (101-105) are solenoid-controlled bright lights. Manual trough with 3 balls (sw30-32) and outhole (sw8).

## Unresolved questions

- Is the I/O enumeration complete for every supported physical/controller variant?
- Which inferred VPX behaviors reflect real hardware, and which are table-script conveniences?
- Are all mechanism home states, sensors, motion constraints, and ball interactions documented?

## Sources

- `legacy.game.specfor`: `games/specfor.json` at the pinned migration revision.
