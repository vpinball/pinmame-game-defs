# Police Force

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

- `games/polic.json#/switches/0._note`: Outhole position — SolTrough (sol 1) kicks from here into sw11
- `games/polic.json#/switches/1._note`: Middle trough — ball stacks here. SolRelease (sol 22) kicks to shooter lane
- `games/polic.json#/switches/2._note`: Top trough — overflow kicks into sw11 via UpdateTroughTimer
- `games/polic.json#/switches/3._note`: Ball in plunger lane. Cleared by SolRelease
- `games/polic.json#/switches/4._inferred_type`: kicker
- `games/polic.json#/switches/4._note`: VUK — captured ball kicked by SaucerTR (sol 8)
- `games/polic.json#/switches/5._inferred_type`: standup_target
- `games/polic.json#/switches/5._note`: STHit(17) — pulsed via STAnimate
- `games/polic.json#/switches/6._inferred_type`: standup_target
- `games/polic.json#/switches/6._note`: STHit(18) — pulsed via STAnimate
- `games/polic.json#/switches/7._inferred_type`: standup_target
- `games/polic.json#/switches/7._note`: STHit(19) — pulsed via STAnimate
- `games/polic.json#/switches/8._inferred_type`: drop_target
- `games/polic.json#/switches/8._note`: DTHit(20) — right bank, reset by sol 4 (dtRightBank)
- `games/polic.json#/switches/9._inferred_type`: drop_target
- `games/polic.json#/switches/9._note`: DTHit(21) — right bank, reset by sol 4 (dtRightBank)
- `games/polic.json#/switches/10._inferred_type`: drop_target
- `games/polic.json#/switches/10._note`: DTHit(22) — right bank, reset by sol 4 (dtRightBank)
- `games/polic.json#/switches/11._inferred_type`: kicker
- `games/polic.json#/switches/11._note`: VUK — captured ball kicked by SaucerRight (sol 5)
- `games/polic.json#/switches/12._inferred_type`: kicker
- `games/polic.json#/switches/12._note`: VUK — captured ball kicked by SaucerTL (sol 2)
- `games/polic.json#/switches/13._inferred_type`: drop_target
- `games/polic.json#/switches/13._note`: DTHit(25) — left bank, reset by sol 6 (dtLeftBank)
- `games/polic.json#/switches/14._inferred_type`: drop_target
- `games/polic.json#/switches/14._note`: DTHit(26) — left bank, reset by sol 6 (dtLeftBank)
- `games/polic.json#/switches/15._inferred_type`: drop_target
- `games/polic.json#/switches/15._note`: DTHit(27) — left bank, reset by sol 6 (dtLeftBank)
- `games/polic.json#/switches/16._inferred_type`: opto
- `games/polic.json#/switches/16._note`: Car mechanism — set when car is at back of ramp (CarLocation <= 10). Driven by SolCar motor (sol 15)
- `games/polic.json#/switches/17._inferred_type`: opto
- `games/polic.json#/switches/17._note`: Car mechanism — set when car is at front of ramp (CarLocation >= CarDistance - 10). Driven by SolCar motor (sol 15)
- `games/polic.json#/switches/18._note`: Pulsed via vpmTimer.PulseSw 34
- `games/polic.json#/switches/19._inferred_type`: standup_target
- `games/polic.json#/switches/19._note`: STHit(35) — pulsed via STAnimate
- `games/polic.json#/switches/20._inferred_type`: opto
- `games/polic.json#/switches/20._note`: Toggled by SolBallDiverter (sol 3). Switch tracks diverter arm position
- `games/polic.json#/switches/21._note`: Pulsed via vpmTimer.PulseSw 37
- `games/polic.json#/switches/22._note`: Pulsed via vpmTimer.PulseSw 38
- `games/polic.json#/switches/23._inferred_type`: spinner
- `games/polic.json#/switches/23._note`: sw41_Spin() — pulsed via vpmTimer.PulseSw 41
- `games/polic.json#/switches/24._note`: Pulsed via vpmTimer.PulseSw 45
- `games/polic.json#/switches/25._note`: Pulsed via vpmTimer.PulseSw 46
- `games/polic.json#/switches/26._note`: Controller.Switch set/cleared on Hit/UnHit
- `games/polic.json#/switches/27._note`: Controller.Switch set/cleared on Hit/UnHit
- `games/polic.json#/switches/28._note`: Controller.Switch set/cleared on Hit/UnHit
- `games/polic.json#/switches/29._note`: Controller.Switch set/cleared on Hit/UnHit
- `games/polic.json#/switches/30._note`: Controller.Switch set/cleared on Hit/UnHit
- `games/polic.json#/switches/31._note`: Controller.Switch set/cleared on Hit/UnHit
- `games/polic.json#/switches/32._note`: Controller.Switch set/cleared on Hit/UnHit
- `games/polic.json#/switches/33._vbscript_name`: swTilt
- `games/polic.json#/switches/33._note`: vpmNudge.TiltSwitch = swTilt (S11.VBS framework constant = 57)
- `games/polic.json#/switches/34._inferred_type`: bumper
- `games/polic.json#/switches/34._note`: Bumper1_Hit — pulsed via vpmTimer.PulseSw 60
- `games/polic.json#/switches/35._inferred_type`: bumper
- `games/polic.json#/switches/35._note`: Bumper2_Hit — pulsed via vpmTimer.PulseSw 61
- `games/polic.json#/switches/36._inferred_type`: bumper
- `games/polic.json#/switches/36._note`: Bumper3_Hit — pulsed via vpmTimer.PulseSw 62
- `games/polic.json#/switches/37._inferred_type`: slingshot
- `games/polic.json#/switches/37._note`: RightSlingShot_Slingshot — pulsed via vpmTimer.PulseSw 63
- `games/polic.json#/switches/38._inferred_type`: slingshot
- `games/polic.json#/switches/38._note`: LeftSlingShot_Slingshot — pulsed via vpmTimer.PulseSw 64
- `games/polic.json#/coils/0._vbscript_callback`: SolTrough
- `games/polic.json#/coils/0._inferred_type`: ball_management
- `games/polic.json#/coils/0._note`: Kicks ball from sw10 (outhole) into trough stack (sw11)
- `games/polic.json#/coils/1._vbscript_callback`: SaucerTL
- `games/polic.json#/coils/1._inferred_type`: kicker
- `games/polic.json#/coils/1._note`: Kicks ball from sw24 (saucer top left)
- `games/polic.json#/coils/2._vbscript_callback`: SolBallDiverter
- `games/polic.json#/coils/2._inferred_type`: diverter
- `games/polic.json#/coils/2._note`: Toggles diverter arm position and Controller.Switch(36)
- `games/polic.json#/coils/3._vbscript_callback`: dtRightBank
- `games/polic.json#/coils/3._inferred_type`: drop_target_reset
- `games/polic.json#/coils/3._note`: Resets drop targets sw20, sw21, sw22
- `games/polic.json#/coils/4._vbscript_callback`: SaucerRight
- `games/polic.json#/coils/4._inferred_type`: kicker
- `games/polic.json#/coils/4._note`: Kicks ball from sw23 (saucer right)
- `games/polic.json#/coils/5._vbscript_callback`: dtLeftBank
- `games/polic.json#/coils/5._inferred_type`: drop_target_reset
- `games/polic.json#/coils/5._note`: Resets drop targets sw25, sw26, sw27
- `games/polic.json#/coils/6._vbscript_callback`: SolKnocker
- `games/polic.json#/coils/6._inferred_type`: knocker
- `games/polic.json#/coils/7._vbscript_callback`: SaucerTR
- `games/polic.json#/coils/7._inferred_type`: kicker
- `games/polic.json#/coils/7._note`: Kicks ball from sw15 (saucer top right)
- `games/polic.json#/coils/8._vbscript_callback`: Flash109 / FlashMod109
- `games/polic.json#/coils/8._inferred_type`: flasher
- `games/polic.json#/coils/8._note`: f109. Has both ModSol (PWM) and non-ModSol callback paths
- `games/polic.json#/coils/9._vbscript_callback`: SolGIBlink / SolModGIBlink
- `games/polic.json#/coils/9._inferred_type`: gi_relay
- `games/polic.json#/coils/9._note`: Playfield GI dimming control. Commented-out non-mod SolCallback in base block, active in both if/else branches
- `games/polic.json#/coils/10._vbscript_callback`: SolBGGIBlink
- `games/polic.json#/coils/10._inferred_type`: gi_relay
- `games/polic.json#/coils/10._note`: BG GI dimming — always active (not in ModSol conditional)
- `games/polic.json#/coils/11._vbscript_callback`: Flash113 / FlashMod113
- `games/polic.json#/coils/11._inferred_type`: flasher
- `games/polic.json#/coils/11._note`: f113. Skill shot insert flasher
- `games/polic.json#/coils/12._vbscript_callback`: Flash114 / FlashMod114
- `games/polic.json#/coils/12._inferred_type`: flasher
- `games/polic.json#/coils/12._note`: f114 / f114a. Two inserts driven by one coil
- `games/polic.json#/coils/13._vbscript_callback`: SolCar
- `games/polic.json#/coils/13._inferred_type`: motor
- `games/polic.json#/coils/13._note`: Drives car mechanism up/down ramp. Controls switches 31 (back) and 32 (front). Plays 'Motor' sound loop
- `games/polic.json#/coils/14._vbscript_callback`: SolRelease
- `games/polic.json#/coils/14._inferred_type`: ball_management
- `games/polic.json#/coils/14._note`: Kicks ball from sw11 to shooter lane. Also clears Controller.Switch(14)
- `games/polic.json#/coils/15._vbscript_callback`: SolGI
- `games/polic.json#/coils/15._inferred_type`: gi_relay
- `games/polic.json#/coils/15._note`: Main playfield GI on/off relay
- `games/polic.json#/coils/16._vbscript_callback`: Flash125 / FlashMod125
- `games/polic.json#/coils/16._inferred_type`: flasher
- `games/polic.json#/coils/16._note`: f125. 1c — bottom left shark dome
- `games/polic.json#/coils/17._vbscript_callback`: Flash126 / FlashMod126
- `games/polic.json#/coils/17._inferred_type`: flasher
- `games/polic.json#/coils/17._note`: f126. 2c — top left croc dome
- `games/polic.json#/coils/18._vbscript_callback`: Flash127 / FlashMod127
- `games/polic.json#/coils/18._inferred_type`: flasher
- `games/polic.json#/coils/18._note`: f127. 3c — center rat dome
- `games/polic.json#/coils/19._vbscript_callback`: Flash128 / FlashMod128
- `games/polic.json#/coils/19._inferred_type`: flasher
- `games/polic.json#/coils/19._note`: f128. 4c — bottom right weasel PF lamp
- `games/polic.json#/coils/20._vbscript_callback`: Flash129 / FlashMod129
- `games/polic.json#/coils/20._inferred_type`: flasher
- `games/polic.json#/coils/20._note`: f129 / f129a. 5c — jackpot insert and scope billboard
- `games/polic.json#/coils/21._vbscript_callback`: Flash130 / FlashMod130
- `games/polic.json#/coils/21._inferred_type`: flasher
- `games/polic.json#/coils/21._note`: f130. 6c — million flasher insert
- `games/polic.json#/coils/22._vbscript_callback`: Flash131 / FlashMod131
- `games/polic.json#/coils/22._inferred_type`: flasher
- `games/polic.json#/coils/22._note`: f131. Left dome — possibly backbox topper
- `games/polic.json#/coils/23._vbscript_callback`: Flash132 / FlashMod132
- `games/polic.json#/coils/23._inferred_type`: flasher
- `games/polic.json#/coils/23._note`: f132. Right dome — possibly backbox topper
- `games/polic.json#/_source/confidence_notes`: High confidence on coils from SolCallback/SolModCallback assignments. High confidence on switches from sw*_Hit/UnHit handlers, PulseSw calls, DTHit/STHit target arrays, and Controller.Switch assignments. Flasher coils (9, 13, 14, 25-32) have both ModSol and non-ModSol paths. Lamps use vpmMapLights with InsertLamps collection (ROM-driven, no explicit lamp IDs in script). Car mechanism (sol 15) drives switches 31/32 via position logic. Trough is manual 3-ball (sw10/11/12) with custom kick logic, not cvpmTrough. Framework constants from S11.VBS: sLRFlipper=46, sLLFlipper=48, swTilt=57.

## Unresolved questions

- Is the I/O enumeration complete for every supported physical/controller variant?
- Which inferred VPX behaviors reflect real hardware, and which are table-script conveniences?
- Are all mechanism home states, sensors, motion constraints, and ball interactions documented?

## Sources

- `legacy.game.polic`: `games/polic.json` at the pinned migration revision.
