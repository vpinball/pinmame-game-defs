# Haunted House

Coverage: **partial - source-derived recreation knowledge requiring validation**

## Overview

Legacy evidence identifies this candidate as Gottlieb (1982). The information below is preserved for recreation work but is not automatically treated as validated physical-machine fact.

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

- `games/hauntedhouse.json#/switches/0._inferred_type`: drop_target
- `games/hauntedhouse.json#/switches/0._note`: Lower/basement playfield drop target bank
- `games/hauntedhouse.json#/switches/1._inferred_type`: bumper
- `games/hauntedhouse.json#/switches/1._note`: Bumper4 (LPF) — pulsed via vpmTimer.PulseSw(1)
- `games/hauntedhouse.json#/switches/2._inferred_type`: drop_target
- `games/hauntedhouse.json#/switches/2._note`: Upper drop target bank (UPF)
- `games/hauntedhouse.json#/switches/3._inferred_type`: standup_target
- `games/hauntedhouse.json#/switches/3._note`: Upper playfield standup
- `games/hauntedhouse.json#/switches/4._note`: Switch — Controller.Switch set/unset on hit/unhit
- `games/hauntedhouse.json#/switches/5._inferred_type`: standup_target
- `games/hauntedhouse.json#/switches/5._note`: Main playfield standup
- `games/hauntedhouse.json#/switches/6._note`: Lower playfield through-lane switch (LPF)
- `games/hauntedhouse.json#/switches/7._inferred_type`: drop_target
- `games/hauntedhouse.json#/switches/7._note`: Lower/basement drop target bank
- `games/hauntedhouse.json#/switches/8._inferred_type`: kicking_target
- `games/hauntedhouse.json#/switches/8._note`: Main playfield kicking target
- `games/hauntedhouse.json#/switches/9._inferred_type`: drop_target
- `games/hauntedhouse.json#/switches/9._note`: Upper drop target bank (UPF)
- `games/hauntedhouse.json#/switches/10._inferred_type`: standup_target
- `games/hauntedhouse.json#/switches/10._note`: Upper playfield standup
- `games/hauntedhouse.json#/switches/11._inferred_type`: kicking_target
- `games/hauntedhouse.json#/switches/11._note`: Main playfield kicking target
- `games/hauntedhouse.json#/switches/12._inferred_type`: standup_target
- `games/hauntedhouse.json#/switches/12._note`: Main playfield standup
- `games/hauntedhouse.json#/switches/13._note`: Lower playfield through-lane switch (LPF)
- `games/hauntedhouse.json#/switches/14._inferred_type`: drop_target
- `games/hauntedhouse.json#/switches/14._note`: Lower/basement drop target bank
- `games/hauntedhouse.json#/switches/15._note`: Switch — Controller.Switch set/unset on hit/unhit (UPF)
- `games/hauntedhouse.json#/switches/16._inferred_type`: drop_target
- `games/hauntedhouse.json#/switches/16._note`: Upper drop target bank (UPF)
- `games/hauntedhouse.json#/switches/17._inferred_type`: standup_target
- `games/hauntedhouse.json#/switches/17._note`: Upper playfield standup
- `games/hauntedhouse.json#/switches/18._inferred_type`: kicking_target
- `games/hauntedhouse.json#/switches/18._note`: Main playfield kicking target
- `games/hauntedhouse.json#/switches/19._inferred_type`: kicking_target
- `games/hauntedhouse.json#/switches/19._note`: Main playfield kicking target
- `games/hauntedhouse.json#/switches/20._note`: Lower playfield through-lane switch (LPF)
- `games/hauntedhouse.json#/switches/21._inferred_type`: drop_target
- `games/hauntedhouse.json#/switches/21._note`: Lower/basement drop target bank
- `games/hauntedhouse.json#/switches/22._inferred_type`: kicker
- `games/hauntedhouse.json#/switches/22._note`: Basement up-kick saucer — kicks ball back up to main playfield. Activated via LampCallback on Controller.Lamp(12)
- `games/hauntedhouse.json#/switches/23._inferred_type`: drop_target
- `games/hauntedhouse.json#/switches/23._note`: Upper drop target bank (UPF)
- `games/hauntedhouse.json#/switches/24._inferred_type`: standup_target
- `games/hauntedhouse.json#/switches/24._note`: Upper playfield standup
- `games/hauntedhouse.json#/switches/25._note`: Switch — Controller.Switch set/unset on hit/unhit (MPF)
- `games/hauntedhouse.json#/switches/26._note`: Gate switch (MPF) — also controls Gate4 damping animation
- `games/hauntedhouse.json#/switches/27._note`: Lower playfield through-lane switch (LPF)
- `games/hauntedhouse.json#/switches/28._inferred_type`: drop_target
- `games/hauntedhouse.json#/switches/28._note`: Lower/basement drop target bank
- `games/hauntedhouse.json#/switches/29._inferred_type`: kicker
- `games/hauntedhouse.json#/switches/29._note`: Basement special saucer — kicked by solenoid 6 (BS callback)
- `games/hauntedhouse.json#/switches/30._inferred_type`: rubber
- `games/hauntedhouse.json#/switches/30._note`: Upper playfield scoring rubber — sw42a and sw42b both pulse sw42. Also sw42b_Hit.
- `games/hauntedhouse.json#/switches/31._inferred_type`: bumper
- `games/hauntedhouse.json#/switches/31._note`: Bumper3 (UPF) — pulsed via vpmTimer.PulseSw(43)
- `games/hauntedhouse.json#/switches/32._inferred_type`: bumper
- `games/hauntedhouse.json#/switches/32._note`: Bumper1 (bottom) and Bumper2 (top) on MPF — both pulse sw44
- `games/hauntedhouse.json#/switches/33._inferred_type`: kicker
- `games/hauntedhouse.json#/switches/33._note`: Main playfield saucer — kicked by solenoid 2 (UpKick callback)
- `games/hauntedhouse.json#/switches/34._inferred_type`: kicker
- `games/hauntedhouse.json#/switches/34._note`: Main playfield saucer — kicked by solenoid 1 (Kick46 callback). Ball starts here at init. Multi-step kick animation with TWKicker1 prim.
- `games/hauntedhouse.json#/switches/35._inferred_type`: standup_target
- `games/hauntedhouse.json#/switches/35._note`: Lower/basement playfield standup
- `games/hauntedhouse.json#/switches/36._inferred_type`: slingshot
- `games/hauntedhouse.json#/switches/36._note`: Lower playfield slingshot — pulsed via vpmTimer.PulseSw(51). Also scoring rubber sw51a/sw51b pulse sw51.
- `games/hauntedhouse.json#/switches/37._note`: Switch — Controller.Switch set/unset on hit/unhit (MPF)
- `games/hauntedhouse.json#/switches/38._inferred_type`: standup_target
- `games/hauntedhouse.json#/switches/38._note`: Main playfield standup
- `games/hauntedhouse.json#/switches/39._note`: Tilt switch — vpmNudge.TiltSwitch = 57
- `games/hauntedhouse.json#/switches/40._inferred_type`: standup_target
- `games/hauntedhouse.json#/switches/40._note`: Lower/basement playfield standup
- `games/hauntedhouse.json#/switches/41._note`: Gate switch (UPF) — also controls Gate3 damping animation
- `games/hauntedhouse.json#/switches/42._note`: Impulse plunger switch — used by plungerIM (cvpmImpulseP). Kicked by lamp 15 via LampCallback.
- `games/hauntedhouse.json#/switches/43._inferred_type`: slingshot
- `games/hauntedhouse.json#/switches/43._note`: Upper playfield slingshot — pulsed via vpmTimer.PulseSw(66). Also sw66b_hit pulses sw66 (main scoring rubber).
- `games/hauntedhouse.json#/switches/44._note`: Single-ball trough kicker. Ball release via solenoid 9 (KickBallToLane). Drain directs ball here.
- `games/hauntedhouse.json#/coils/0._vbscript_callback`: Kick46
- `games/hauntedhouse.json#/coils/0._inferred_type`: kicker
- `games/hauntedhouse.json#/coils/0._note`: Kicks ball from sw46 saucer with multi-step animation (TWKicker1 prim). Ball start position.
- `games/hauntedhouse.json#/coils/1._vbscript_callback`: UpKick
- `games/hauntedhouse.json#/coils/1._inferred_type`: kicker
- `games/hauntedhouse.json#/coils/1._note`: Kicks ball from sw45 saucer on main playfield
- `games/hauntedhouse.json#/coils/2._vbscript_callback`: UpperDropsUp
- `games/hauntedhouse.json#/coils/2._inferred_type`: drop_target_reset
- `games/hauntedhouse.json#/coils/2._note`: Raises all four upper drop targets (sw2, sw12, sw22, sw32)
- `games/hauntedhouse.json#/coils/3._vbscript_callback`: BS
- `games/hauntedhouse.json#/coils/3._inferred_type`: kicker
- `games/hauntedhouse.json#/coils/3._note`: Kicks ball from sw41 basement special saucer
- `games/hauntedhouse.json#/coils/4._vbscript_callback`: PlayKnocker
- `games/hauntedhouse.json#/coils/4._inferred_type`: knocker
- `games/hauntedhouse.json#/coils/5._vbscript_callback`: KickBallToLane
- `games/hauntedhouse.json#/coils/5._inferred_type`: ball_management
- `games/hauntedhouse.json#/coils/5._note`: Kicks ball from Kicker1 (sw67 trough) to shooter lane
- `games/hauntedhouse.json#/coils/6._vbscript_callback`: GameOver
- `games/hauntedhouse.json#/coils/6._inferred_type`: game_on
- `games/hauntedhouse.json#/coils/6._note`: Sets GameInPlay flag — controls whether upper/lower flippers can activate
- `games/hauntedhouse.json#/coils/7._vbscript_callback`: SolGi
- `games/hauntedhouse.json#/coils/7._inferred_type`: gi_relay
- `games/hauntedhouse.json#/coils/7._note`: Controls GI relay sound effect only — actual GI switching done via Controller.Lamp(17) in LampCallback
- `games/hauntedhouse.json#/coils/8._vbscript_callback`: SolRFlipper
- `games/hauntedhouse.json#/coils/8._inferred_type`: flipper
- `games/hauntedhouse.json#/coils/8._note`: Main right flipper (RightFlipper/RightFlipper2). Also cascades to SolRUFlipper when FlipperKeyMod=2.
- `games/hauntedhouse.json#/coils/9._vbscript_callback`: SolLFlipper
- `games/hauntedhouse.json#/coils/9._inferred_type`: flipper
- `games/hauntedhouse.json#/coils/9._note`: Main left flipper (LeftFlipper/LeftFlipper2). Also cascades to SolLUFlipper when FlipperKeyMod=2.
- `games/hauntedhouse.json#/lamps/0._playfield`: UPF
- `games/hauntedhouse.json#/lamps/1._playfield`: MPF
- `games/hauntedhouse.json#/lamps/2._playfield`: MPF
- `games/hauntedhouse.json#/lamps/2._note`: Near sw55 standup target area and upper slingshot
- `games/hauntedhouse.json#/lamps/3._playfield`: MPF
- `games/hauntedhouse.json#/lamps/3._note`: Near secret target area and lower left region
- `games/hauntedhouse.json#/lamps/4._playfield`: MPF
- `games/hauntedhouse.json#/lamps/5._playfield`: MPF
- `games/hauntedhouse.json#/lamps/6._playfield`: UPF
- `games/hauntedhouse.json#/lamps/6._note`: Near upper rubber/sling area
- `games/hauntedhouse.json#/lamps/7._playfield`: MPF
- `games/hauntedhouse.json#/lamps/8._playfield`: LPF
- `games/hauntedhouse.json#/lamps/8._note`: Positioned in Backdrop_Init for desktop mode
- `games/hauntedhouse.json#/lamps/9._playfield`: LPF
- `games/hauntedhouse.json#/lamps/9._note`: Positioned in Backdrop_Init for desktop mode
- `games/hauntedhouse.json#/lamps/10._playfield`: LPF
- `games/hauntedhouse.json#/lamps/10._note`: Near sw60 standup target. Positioned in Backdrop_Init.
- `games/hauntedhouse.json#/lamps/11._playfield`: LPF
- `games/hauntedhouse.json#/lamps/11._note`: Positioned in Backdrop_Init for desktop mode
- `games/hauntedhouse.json#/lamps/12._playfield`: MPF
- `games/hauntedhouse.json#/lamps/13._playfield`: MPF
- `games/hauntedhouse.json#/lamps/14._playfield`: MPF
- `games/hauntedhouse.json#/lamps/15._playfield`: MPF
- `games/hauntedhouse.json#/lamps/15._note`: Near sw20/sw30 lower drop target area
- `games/hauntedhouse.json#/lamps/16._playfield`: MPF
- `games/hauntedhouse.json#/lamps/17._playfield`: MPF
- `games/hauntedhouse.json#/lamps/18._playfield`: MPF
- `games/hauntedhouse.json#/lamps/19._playfield`: MPF
- `games/hauntedhouse.json#/lamps/20._playfield`: MPF
- `games/hauntedhouse.json#/lamps/20._note`: Near lower left/right flipper area and secret target
- `games/hauntedhouse.json#/lamps/21._playfield`: MPF
- `games/hauntedhouse.json#/lamps/22._playfield`: MPF
- `games/hauntedhouse.json#/lamps/23._playfield`: MPF
- `games/hauntedhouse.json#/lamps/24._playfield`: MPF
- `games/hauntedhouse.json#/lamps/24._note`: Near upper slingshot area
- `games/hauntedhouse.json#/lamps/25._playfield`: UPF
- `games/hauntedhouse.json#/lamps/25._note`: Near sw13 standup target
- `games/hauntedhouse.json#/lamps/26._playfield`: UPF
- `games/hauntedhouse.json#/lamps/26._note`: Near sw13/sw23/sw33 standup targets
- `games/hauntedhouse.json#/lamps/27._playfield`: UPF
- `games/hauntedhouse.json#/lamps/27._note`: Near sw33 standup target
- `games/hauntedhouse.json#/lamps/28._playfield`: UPF
- `games/hauntedhouse.json#/lamps/29._playfield`: LPF
- `games/hauntedhouse.json#/lamps/29._note`: Positioned in Backdrop_Init for desktop mode
- `games/hauntedhouse.json#/lamps/30._playfield`: MPF
- `games/hauntedhouse.json#/lamps/30._note`: Near sw34 rollover area
- `games/hauntedhouse.json#/lamps/31._playfield`: MPF
- `games/hauntedhouse.json#/lamps/31._note`: Near trap door and Gate3 area
- `games/hauntedhouse.json#/lamps/32._playfield`: MPF
- `games/hauntedhouse.json#/lamps/32._note`: Near sw05/sw15 standup target area and lower right flipper region
- `games/hauntedhouse.json#/gi/0`: Unbound legacy outputs record `giUL1` was retained as a migration note only.
- `games/hauntedhouse.json#/gi/0._playfield`: UPF
- `games/hauntedhouse.json#/gi/0._note`: Part of GIUpper array — controlled by GI relay state
- `games/hauntedhouse.json#/gi/1`: Unbound legacy outputs record `giUL2` was retained as a migration note only.
- `games/hauntedhouse.json#/gi/1._playfield`: UPF
- `games/hauntedhouse.json#/gi/1._note`: Part of GIUpper array — listed as 'gUL2' in VLM (typo)
- `games/hauntedhouse.json#/gi/2`: Unbound legacy outputs record `giUL3` was retained as a migration note only.
- `games/hauntedhouse.json#/gi/2._playfield`: UPF
- `games/hauntedhouse.json#/gi/3`: Unbound legacy outputs record `giUL4` was retained as a migration note only.
- `games/hauntedhouse.json#/gi/3._playfield`: UPF
- `games/hauntedhouse.json#/gi/4`: Unbound legacy outputs record `giUL5` was retained as a migration note only.
- `games/hauntedhouse.json#/gi/4._playfield`: UPF
- `games/hauntedhouse.json#/gi/5`: Unbound legacy outputs record `giUL6` was retained as a migration note only.
- `games/hauntedhouse.json#/gi/5._playfield`: UPF
- `games/hauntedhouse.json#/gi/6`: Unbound legacy outputs record `giML1` was retained as a migration note only.
- `games/hauntedhouse.json#/gi/6._playfield`: MPF
- `games/hauntedhouse.json#/gi/6._note`: Part of GIMain array — controlled by GI relay state
- `games/hauntedhouse.json#/gi/7`: Unbound legacy outputs record `giML2` was retained as a migration note only.
- `games/hauntedhouse.json#/gi/7._playfield`: MPF
- `games/hauntedhouse.json#/gi/8`: Unbound legacy outputs record `giML3` was retained as a migration note only.
- `games/hauntedhouse.json#/gi/8._playfield`: MPF
- `games/hauntedhouse.json#/gi/9`: Unbound legacy outputs record `giML4` was retained as a migration note only.
- `games/hauntedhouse.json#/gi/9._playfield`: MPF
- `games/hauntedhouse.json#/gi/10`: Unbound legacy outputs record `giML5` was retained as a migration note only.
- `games/hauntedhouse.json#/gi/10._playfield`: MPF
- `games/hauntedhouse.json#/gi/11`: Unbound legacy outputs record `giML6` was retained as a migration note only.
- `games/hauntedhouse.json#/gi/11._playfield`: MPF
- `games/hauntedhouse.json#/gi/12`: Unbound legacy outputs record `giLL1` was retained as a migration note only.
- `games/hauntedhouse.json#/gi/12._playfield`: LPF
- `games/hauntedhouse.json#/gi/12._note`: Part of GILower array — only GI string for basement. ON when GI relay on (Lamp 17 = 1), OFF when relay off.
- `games/hauntedhouse.json#/lamp_coils/0._inferred_type`: kicker
- `games/hauntedhouse.json#/lamp_coils/0._note`: Lamp used as coil via LampCallback. When Controller.Lamp(12) turns on, kicks ball from sw31 basement saucer.
- `games/hauntedhouse.json#/lamp_coils/1._inferred_type`: drop_target_reset
- `games/hauntedhouse.json#/lamp_coils/1._note`: Lamp used as coil via LampCallback. When Controller.Lamp(13) turns on, raises all five lower drop targets (sw0, sw10, sw20, sw30, sw40).
- `games/hauntedhouse.json#/lamp_coils/2._inferred_type`: kicker
- `games/hauntedhouse.json#/lamp_coils/2._note`: Lamp used as coil via LampCallback. When Controller.Lamp(15) turns on, fires plungerIM (cvpmImpulseP) auto-fire.
- `games/hauntedhouse.json#/lamp_coils/3._inferred_type`: trap_door
- `games/hauntedhouse.json#/lamp_coils/3._note`: Lamp used as coil via LampCallback. On = opens trap door (TrapDoorR not collidable), Off = closes trap door. Animated with TrapDoorTimer.
- `games/hauntedhouse.json#/lamp_coils/4._inferred_type`: gi_relay
- `games/hauntedhouse.json#/lamp_coils/4._note`: Lamp used as coil via LampCallback. On = SolGIOn (lower PF lit, upper+main off). Off = SolGIOff (upper+main lit, lower off). Also gates upper/lower flipper activation.
- `games/hauntedhouse.json#/_source/confidence_notes`: High confidence on switches/coils from SolCallback and Controller.Switch handlers. Uses sys80.VBS (Gottlieb System 80). Three-playfield design (Upper, Main, Lower/Basement) — unique architecture for 1982. Lamp numbers inferred from VLM insert array naming (LM_inserts_{playfield}_l{N}) and Backdrop_Init light object names. Lamps 12/13/15/16/17 are used as coil outputs via LampCallback (lamp-as-solenoid pattern common on System 80). No cvpmTrough — single-ball physical trough with Kicker1 (sw67). Ball starts in sw46 kicker (main playfield saucer) at init. Upper flippers (FlipperUL/FlipperUR) and basement flippers (FlipperLL/FlipperLR) are controlled via MagnaSave keys, not via separate SolCallbacks — they are VBS-only, activated when Controller.Lamp(17) is on (GI state). GI relay (sol 11) controls which playfield is lit: off = upper+main lit, on = lower/basement lit. UseSolenoids=2 (modulated), UseLamps=1, UseGI=0.

## Unresolved questions

- Is the I/O enumeration complete for every supported physical/controller variant?
- Which inferred VPX behaviors reflect real hardware, and which are table-script conveniences?
- Are all mechanism home states, sensors, motion constraints, and ball interactions documented?

## Sources

- `legacy.game.hauntedhouse`: `games/hauntedhouse.json` at the pinned migration revision.
