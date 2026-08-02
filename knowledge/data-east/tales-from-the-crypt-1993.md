# Tales from the Crypt

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

- `games/tftc.json#/switches/0._note`: vpmNudge.TiltSwitch = 1
- `games/tftc.json#/switches/1._note`: Pulsed via keyFront (2 key). vpmTimer.PulseSw 8
- `games/tftc.json#/switches/2._note`: Custom trough. Controller.Switch on/off. Drain kicker — balls cascade from here through sw10-sw14 to sw15.
- `games/tftc.json#/switches/3._note`: Custom trough. Controller.Switch on/off.
- `games/tftc.json#/switches/4._note`: Custom trough. Controller.Switch on/off.
- `games/tftc.json#/switches/5._note`: Custom trough. Controller.Switch on/off.
- `games/tftc.json#/switches/6._note`: Custom trough. Controller.Switch on/off.
- `games/tftc.json#/switches/7._note`: Custom trough. Controller.Switch on/off. kisort (coil 1) kicks from here.
- `games/tftc.json#/switches/8._note`: Custom trough. Controller.Switch on/off. KickBallToLane (coil 2) kicks ball from here to plunger lane. Also mTombStone.Sol1 = 15 (tombstone mechanism uses this solenoid number).
- `games/tftc.json#/switches/9._note`: Controller.Switch on/off. Sets BIPL (Ball In Plunger Lane) flag.
- `games/tftc.json#/switches/10._note`: Controller.Switch on/off.
- `games/tftc.json#/switches/11._note`: Controller.Switch on/off.
- `games/tftc.json#/switches/12._note`: vpmTimer.PulseSw 19 in LeftSlingShot_Slingshot sub.
- `games/tftc.json#/switches/13._note`: vpmTimer.PulseSw(20). Animated standup target with TargetBouncer.
- `games/tftc.json#/switches/14._note`: vpmTimer.PulseSw(21). Animated standup target with TargetBouncer.
- `games/tftc.json#/switches/15._note`: vpmTimer.PulseSw(22). Animated standup target with TargetBouncer.
- `games/tftc.json#/switches/16._note`: Controller.Switch on/off.
- `games/tftc.json#/switches/17._note`: Controller.Switch on/off.
- `games/tftc.json#/switches/18._note`: Controller.Switch on/off.
- `games/tftc.json#/switches/19._note`: Controller.Switch on/off.
- `games/tftc.json#/switches/20._note`: vpmTimer.PulseSw 27 in RightSlingShot_Slingshot sub.
- `games/tftc.json#/switches/21._note`: vpmTimer.PulseSw(28). Animated standup target with TargetBouncer.
- `games/tftc.json#/switches/22._note`: vpmTimer.PulseSw(29). Animated standup target with TargetBouncer.
- `games/tftc.json#/switches/23._note`: vpmTimer.PulseSw(30). Animated standup target with TargetBouncer.
- `games/tftc.json#/switches/24._note`: Controller.Switch on/off.
- `games/tftc.json#/switches/25._note`: Controller.Switch on/off.
- `games/tftc.json#/switches/26._note`: mTombStone.AddSw 33, 160, 180. cvpmMech switch — tombstone at raised/up position.
- `games/tftc.json#/switches/27._note`: mTombStone.AddSw 36, 0, 20. cvpmMech switch — tombstone at lowered/down position.
- `games/tftc.json#/switches/28._note`: Controller.Switch on/off. Ball enters pUpKicker area. KickBallUp38 (coil 6) ejects.
- `games/tftc.json#/switches/29._note`: vpmTimer.PulseSw 39.
- `games/tftc.json#/switches/30._note`: DTHit 41 via sw41w_Hit. Custom drop target animation code sets Controller.Switch(41) on drop, clears on raise.
- `games/tftc.json#/switches/31._note`: DTHit 42 via sw42w_Hit. Custom drop target animation code sets Controller.Switch(42) on drop, clears on raise.
- `games/tftc.json#/switches/32._note`: DTHit 43 via sw43w_Hit. Custom drop target animation code sets Controller.Switch(43) on drop, clears on raise.
- `games/tftc.json#/switches/33._note`: vpmTimer.PulseSw 44.
- `games/tftc.json#/switches/34._note`: Controller.Switch on/off. Animated switch (switch01 roty).
- `games/tftc.json#/switches/35._note`: vpmTimer.PulseSw 46.
- `games/tftc.json#/switches/36._note`: Controller.Switch on/off. Animated switch (switch02 roty).
- `games/tftc.json#/switches/37._note`: vpmTimer.PulseSw(49) in Bumper1_Hit.
- `games/tftc.json#/switches/38._note`: vpmTimer.PulseSw(50) in Bumper2_Hit.
- `games/tftc.json#/switches/39._note`: vpmTimer.PulseSw(51) in Bumper3_Hit.
- `games/tftc.json#/switches/40._note`: Controller.Switch on/off. Ball enters subway VUK. KickBallUp52 (coil 7) ejects.
- `games/tftc.json#/switches/41._note`: Controller.Switch on/off. Ball lock position.
- `games/tftc.json#/switches/42._note`: Controller.Switch on/off. Ball lock position.
- `games/tftc.json#/switches/43._note`: Controller.Switch on/off. ScoopKick (coil 5) ejects.
- `games/tftc.json#/switches/44._note`: Controller.Switch on/off. Animated switch (switch03 roty).
- `games/tftc.json#/switches/45._note`: Controller.Switch set via PlungerKey/LockBarKey in Table1_KeyDown/KeyUp.
- `games/tftc.json#/coils/0._vbscript_callback`: kisort
- `games/tftc.json#/coils/0._inferred_type`: ball_management
- `games/tftc.json#/coils/0._note`: Kicks ball from sw14 toward sw15/shooter lane. Part of custom trough cascade system.
- `games/tftc.json#/coils/1._vbscript_callback`: KickBallToLane
- `games/tftc.json#/coils/1._inferred_type`: ball_management
- `games/tftc.json#/coils/1._note`: Kicks ball from sw15 into plunger lane. Clears Controller.Switch(15).
- `games/tftc.json#/coils/2._vbscript_callback`: Auto_Plunger
- `games/tftc.json#/coils/2._inferred_type`: ball_management
- `games/tftc.json#/coils/2._note`: PlungerIM.AutoFire. Fires ball from plunger lane to playfield.
- `games/tftc.json#/coils/3._vbscript_callback`: ResetDrops
- `games/tftc.json#/coils/3._inferred_type`: mechanism
- `games/tftc.json#/coils/3._note`: Resets drop targets 41/42/43 to raised position.
- `games/tftc.json#/coils/4._vbscript_callback`: ScoopKick
- `games/tftc.json#/coils/4._inferred_type`: ball_management
- `games/tftc.json#/coils/4._note`: Kicks ball from scoop (sw55). Clears Controller.Switch(55).
- `games/tftc.json#/coils/5._vbscript_callback`: KickBallUp38
- `games/tftc.json#/coils/5._inferred_type`: ball_management
- `games/tftc.json#/coils/5._note`: Ejects ball from center VUK (sw38) via timer animation sequence.
- `games/tftc.json#/coils/6._vbscript_callback`: KickBallUp52
- `games/tftc.json#/coils/6._inferred_type`: ball_management
- `games/tftc.json#/coils/6._note`: Ejects ball from back subway VUK (sw52) via timer animation sequence.
- `games/tftc.json#/coils/7._vbscript_callback`: vpmSolSound SoundFX("Knocker",DOFKnocker),
- `games/tftc.json#/coils/7._inferred_type`: knocker
- `games/tftc.json#/coils/8._vbscript_callback`: SolDiv
- `games/tftc.json#/coils/8._inferred_type`: diverter
- `games/tftc.json#/coils/8._note`: Diverter.IsDropped toggled. Animated via timer.
- `games/tftc.json#/coils/9._vbscript_callback`: SetGI
- `games/tftc.json#/coils/9._inferred_type`: gi_relay
- `games/tftc.json#/coils/9._note`: Inverted: solenoid ON cuts GI circuit (GI off). Solenoid OFF enables GI. Controls lamp 111 (GI collection) and bumper top intensities. Early Data East era relay.
- `games/tftc.json#/coils/10._vbscript_callback`: SolShake
- `games/tftc.json#/coils/10._inferred_type`: mechanism
- `games/tftc.json#/coils/10._note`: ShakerMotor.Enabled toggled.
- `games/tftc.json#/coils/11._vbscript_callback`: Solkickback
- `games/tftc.json#/coils/11._inferred_type`: mechanism
- `games/tftc.json#/coils/11._note`: Left outlane kickback. plunger1.Fire/PullBack.
- `games/tftc.json#/coils/12._vbscript_callback`: Sol1R
- `games/tftc.json#/coils/12._inferred_type`: flasher
- `games/tftc.json#/coils/12._note`: Flasher relay. DisableLightingFlash on p65/p65bulb primitives.
- `games/tftc.json#/coils/13._vbscript_callback`: Sol2R
- `games/tftc.json#/coils/13._inferred_type`: flasher
- `games/tftc.json#/coils/13._note`: Flasher relay. Also syncs with GI state (Sol2RGIsync).
- `games/tftc.json#/coils/14._vbscript_callback`: Sol3R
- `games/tftc.json#/coils/14._inferred_type`: flasher
- `games/tftc.json#/coils/14._note`: Flasher relay. DisableLightingFlash on p67/p67bulb and p67a/p67abulb.
- `games/tftc.json#/coils/15._vbscript_callback`: Sol4R
- `games/tftc.json#/coils/15._inferred_type`: flasher
- `games/tftc.json#/coils/15._note`: Flasher relay. Also syncs with GI state (Sol4RGIsync).
- `games/tftc.json#/coils/16._vbscript_callback`: Sol5R
- `games/tftc.json#/coils/16._inferred_type`: flasher
- `games/tftc.json#/coils/16._note`: Flasher relay. DisableLightingFlash on p69b/p69bbulb.
- `games/tftc.json#/coils/17._vbscript_callback`: Sol6R
- `games/tftc.json#/coils/17._inferred_type`: flasher
- `games/tftc.json#/coils/17._note`: Flasher relay. DisableLightingFlash on p70/p70bulb and p70a/p70abulb.
- `games/tftc.json#/coils/18._vbscript_callback`: Sol7R
- `games/tftc.json#/coils/18._inferred_type`: flasher
- `games/tftc.json#/coils/18._note`: Flasher relay. DisableLightingFlash on p71/p71bulb and p60/p60bulb.
- `games/tftc.json#/coils/19._vbscript_callback`: Sol8R
- `games/tftc.json#/coils/19._inferred_type`: flasher
- `games/tftc.json#/coils/19._note`: Flasher relay. DisableLightingFlash on p52/p52bulb.
- `games/tftc.json#/lamps/4._note`: Also has flasher object f5TOP
- `games/tftc.json#/lamps/12._note`: Flasher object. Also F13Light. Callback: g02_bulb2/g02_bulbOFF2
- `games/tftc.json#/lamps/13._note`: Plunger LED. Also F15, f_bulbshooter, PlungerEye1, PlungerEye2
- `games/tftc.json#/lamps/14._note`: Also has l17a secondary object
- `games/tftc.json#/lamps/23._note`: Also has l26a and f26aTOP secondary objects
- `games/tftc.json#/lamps/38._note`: Also has flasher object f41TOP
- `games/tftc.json#/lamps/39._note`: Also has flasher object f42TOP
- `games/tftc.json#/lamps/40._note`: Also has flasher object f43TOP
- `games/tftc.json#/lamps/50._note`: Also has flasher object f53TOP
- `games/tftc.json#/lamps/54._note`: Also l57a. Bumpertop1 callback.
- `games/tftc.json#/lamps/55._note`: Also l58a. Bumpertop2 callback.
- `games/tftc.json#/lamps/56._note`: Also l59a. Bumpertop3 callback.
- `games/tftc.json#/lamps/59._note`: Flasher object. Also F62Light. Callback: g02_bulb1/g02_bulbOFF1
- `games/tftc.json#/lamps/60._note`: Flasher object. Also F63Light. Callback: g02_bulb3/g02_bulbOFF3
- `games/tftc.json#/lamps/62._note`: Lampz GI collection. Controlled by coil 11 (inverted relay). state(111) set via SetLamp.
- `games/tftc.json#/_source/confidence_notes`: High confidence on switches/coils. No Const sw* definitions — switches identified from _Hit/_UnHit subs, Controller.Switch() calls, PulseSw calls, and mechanism AddSw. Custom ball-through system (not cvpmTrough) with 6 kicker positions (Drain + sw10-sw14) and sw15 as shooter lane release. Tombstone is a cvpmMech (Sol1=15, mechanism switches 33 and 36). Drop targets use custom DTHit/DTAnimate code with Controller.Switch set on drop/raise. Flashers (coils 25-32) use Sol1R-Sol8R custom subs with DisableLightingFlash primitives. Lamps use Lampz class with MassAssign. GI controlled via coil 11 (inverted relay — solenoid cuts GI circuit). UseSolenoids=2, UseLamps=0, UseGI=0.

## Unresolved questions

- Is the I/O enumeration complete for every supported physical/controller variant?
- Which inferred VPX behaviors reflect real hardware, and which are table-script conveniences?
- Are all mechanism home states, sensors, motion constraints, and ball interactions documented?

## Sources

- `legacy.game.tftc`: `games/tftc.json` at the pinned migration revision.
