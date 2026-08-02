# X-Men LE

Coverage: **partial - source-derived recreation knowledge requiring validation**

## Overview

Legacy evidence identifies this candidate as Stern (2012). The information below is preserved for recreation work but is not automatically treated as validated physical-machine fact.

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

- `platforms/sam.json#/coils/2`: Unbound legacy outputs record `c_flipper_upper_right` was retained as a migration note only.
- `platforms/sam.json#/coils/3`: Unbound legacy outputs record `c_flipper_upper_left` was retained as a migration note only.
- `games/xmen.json#/switches/0._inferred_type`: drop_target
- `games/xmen.json#/switches/0._note`: PulseSw 1 on hit
- `games/xmen.json#/switches/1._inferred_type`: drop_target
- `games/xmen.json#/switches/1._note`: PulseSw 2 on hit
- `games/xmen.json#/switches/2._inferred_type`: kicker
- `games/xmen.json#/switches/2._note`: Ball captured via Controller.Switch(4)=1, ejected by SolOutLHole (sol 3)
- `games/xmen.json#/switches/3._inferred_type`: drop_target
- `games/xmen.json#/switches/3._note`: PulseSw 7 on hit
- `games/xmen.json#/switches/4._inferred_type`: drop_target
- `games/xmen.json#/switches/4._note`: PulseSw 8 on hit
- `games/xmen.json#/switches/5._inferred_type`: opto
- `games/xmen.json#/switches/5._note`: PulseSw 11
- `games/xmen.json#/switches/6._inferred_type`: opto
- `games/xmen.json#/switches/6._note`: Set to 1 when left Nightcrawler reaches min position, cleared on move up. No VPX trigger — controlled by LeftNightCrawlerWall_Timer mechanism
- `games/xmen.json#/switches/7._inferred_type`: opto
- `games/xmen.json#/switches/7._note`: PulseSw 13
- `games/xmen.json#/switches/8._inferred_type`: rollover
- `games/xmen.json#/switches/9._inferred_type`: cabinet_switch
- `games/xmen.json#/switches/9._note`: Set via vpmKeyDown/vpmKeyUp (StartGameKey)
- `games/xmen.json#/switches/10._inferred_type`: trough
- `games/xmen.json#/switches/11._inferred_type`: trough
- `games/xmen.json#/switches/12._inferred_type`: trough
- `games/xmen.json#/switches/13._inferred_type`: trough
- `games/xmen.json#/switches/14._inferred_type`: rollover
- `games/xmen.json#/switches/15._inferred_type`: rollover
- `games/xmen.json#/switches/16._inferred_type`: rollover
- `games/xmen.json#/switches/16._note`: Ball velocity dampened on hit
- `games/xmen.json#/switches/17._inferred_type`: slingshot
- `games/xmen.json#/switches/17._note`: Triggered via LeftSlingShot_Slingshot, PulseSw 26
- `games/xmen.json#/switches/18._inferred_type`: slingshot
- `games/xmen.json#/switches/18._note`: Triggered via RightSlingShot_Slingshot, PulseSw 27
- `games/xmen.json#/switches/19._inferred_type`: rollover
- `games/xmen.json#/switches/19._note`: Ball velocity dampened on hit
- `games/xmen.json#/switches/20._inferred_type`: rollover
- `games/xmen.json#/switches/21._inferred_type`: bumper
- `games/xmen.json#/switches/21._note`: Triggered via Bumper2b_Hit, PulseSw 30
- `games/xmen.json#/switches/22._inferred_type`: bumper
- `games/xmen.json#/switches/22._note`: Triggered via Bumper1b_Hit, PulseSw 31
- `games/xmen.json#/switches/23._inferred_type`: bumper
- `games/xmen.json#/switches/23._note`: Triggered via Bumper3b_Hit, PulseSw 32
- `games/xmen.json#/switches/24._inferred_type`: rollover
- `games/xmen.json#/switches/24._note`: Ball velocity dampened on hit
- `games/xmen.json#/switches/25._inferred_type`: opto
- `games/xmen.json#/switches/25._note`: Set when Iceman ramp reaches minimum angle (14 deg). Managed by TimerIceManMotor
- `games/xmen.json#/switches/26._inferred_type`: opto
- `games/xmen.json#/switches/26._note`: Set when Iceman ramp reaches maximum angle (60 deg). Managed by TimerIceManMotor
- `games/xmen.json#/switches/27._inferred_type`: standup_target
- `games/xmen.json#/switches/27._note`: PulseSw 36, triggers Wolverine wobble animation
- `games/xmen.json#/switches/28._inferred_type`: rollover
- `games/xmen.json#/switches/29._inferred_type`: rollover
- `games/xmen.json#/switches/30._inferred_type`: rollover
- `games/xmen.json#/switches/31._inferred_type`: standup_target
- `games/xmen.json#/switches/31._note`: PulseSw 41, has visual pop primitive sw41p
- `games/xmen.json#/switches/32._inferred_type`: standup_target
- `games/xmen.json#/switches/32._note`: PulseSw 42, has visual pop primitive sw42p
- `games/xmen.json#/switches/33._inferred_type`: spinner
- `games/xmen.json#/switches/33._note`: PulseSw 47 on spin event
- `games/xmen.json#/switches/34._inferred_type`: rollover
- `games/xmen.json#/switches/34._note`: PulseSw 48
- `games/xmen.json#/switches/35._inferred_type`: rollover
- `games/xmen.json#/switches/36._inferred_type`: wall_switch
- `games/xmen.json#/switches/36._note`: Ball detect on left Nightcrawler toy
- `games/xmen.json#/switches/37._inferred_type`: wall_switch
- `games/xmen.json#/switches/37._note`: Ball detect on right Nightcrawler toy
- `games/xmen.json#/switches/38._inferred_type`: rollover
- `games/xmen.json#/switches/38._note`: Ball on Iceman ramp
- `games/xmen.json#/switches/39._inferred_type`: rollover
- `games/xmen.json#/switches/40._inferred_type`: rollover
- `games/xmen.json#/switches/41._inferred_type`: kicker
- `games/xmen.json#/switches/41._note`: Ball captured via Controller.Switch(55)=1, ejected by SolOutL (sol 5)
- `games/xmen.json#/switches/42._inferred_type`: opto
- `games/xmen.json#/switches/42._note`: Set to 1 when right Nightcrawler reaches min position, cleared on move up. Controlled by RightNightCrawlerWall_Timer mechanism
- `games/xmen.json#/switches/43._inferred_type`: cabinet_switch
- `games/xmen.json#/switches/43._note`: vpmNudge.TiltSwitch = -7 (active low)
- `games/xmen.json#/coils/0._vbscript_callback`: SolRelease
- `games/xmen.json#/coils/0._inferred_type`: ball_management
- `games/xmen.json#/coils/0._note`: Kicks from sw21 (trough position 1)
- `games/xmen.json#/coils/1._vbscript_callback`: solAutofire
- `games/xmen.json#/coils/1._inferred_type`: ball_management
- `games/xmen.json#/coils/1._note`: cvpmImpulseP autofire from swplunger kicker
- `games/xmen.json#/coils/2._vbscript_callback`: SolOutLHole
- `games/xmen.json#/coils/2._inferred_type`: kicker
- `games/xmen.json#/coils/2._note`: Ejects ball from sw4 (Magneto kicker)
- `games/xmen.json#/coils/3._vbscript_callback`: SolMagnetoMagnet
- `games/xmen.json#/coils/3._inferred_type`: magnet
- `games/xmen.json#/coils/3._note`: SolModCallback — modulated magnet. cvpmMagnet on Magnet3 object. Strength proportional to PWM value
- `games/xmen.json#/coils/4._vbscript_callback`: SolOutL
- `games/xmen.json#/coils/4._inferred_type`: kicker
- `games/xmen.json#/coils/4._note`: Ejects ball from sw55 (Magneto lock kicker)
- `games/xmen.json#/coils/5._vbscript_callback`: CLockUp
- `games/xmen.json#/coils/5._inferred_type`: mechanism
- `games/xmen.json#/coils/5._note`: Raises lockPin1 and lockPin2, disables MagnetHelper
- `games/xmen.json#/coils/6._vbscript_callback`: CLockLatch
- `games/xmen.json#/coils/6._inferred_type`: mechanism
- `games/xmen.json#/coils/6._note`: Starts timed latch release for lockPin1
- `games/xmen.json#/coils/7._vbscript_callback`: SolLFlipper
- `games/xmen.json#/coils/7._inferred_type`: flipper
- `games/xmen.json#/coils/8._vbscript_callback`: SolRFlipper
- `games/xmen.json#/coils/8._inferred_type`: flipper
- `games/xmen.json#/coils/8._note`: Also drives RightFlipper1 (upper right flipper)
- `games/xmen.json#/coils/9._vbscript_callback`: SetLampMod 117
- `games/xmen.json#/coils/9._inferred_type`: flasher
- `games/xmen.json#/coils/9._note`: SolModCallback — maps to Lampz index 117
- `games/xmen.json#/coils/10._vbscript_callback`: SetLampMod 118
- `games/xmen.json#/coils/10._inferred_type`: flasher
- `games/xmen.json#/coils/10._note`: SolModCallback — maps to Lampz index 118
- `games/xmen.json#/coils/11._vbscript_callback`: SetLampMod 119
- `games/xmen.json#/coils/11._inferred_type`: flasher
- `games/xmen.json#/coils/11._note`: SolModCallback — maps to Lampz index 119
- `games/xmen.json#/coils/12._vbscript_callback`: SetLampMod 120
- `games/xmen.json#/coils/12._inferred_type`: flasher
- `games/xmen.json#/coils/12._note`: SolModCallback — maps to Lampz index 120
- `games/xmen.json#/coils/13._vbscript_callback`: SetLampMod 121
- `games/xmen.json#/coils/13._inferred_type`: flasher
- `games/xmen.json#/coils/13._note`: SolModCallback — maps to Lampz index 121
- `games/xmen.json#/coils/14._vbscript_callback`: SetLampMod 122
- `games/xmen.json#/coils/14._inferred_type`: flasher
- `games/xmen.json#/coils/14._note`: SolModCallback — maps to Lampz index 122
- `games/xmen.json#/coils/15._vbscript_callback`: solDiscMotor
- `games/xmen.json#/coils/15._inferred_type`: motor
- `games/xmen.json#/coils/15._note`: Drives cvpmTurntable. LE-only feature
- `games/xmen.json#/coils/16._vbscript_callback`: SetLampMod 125
- `games/xmen.json#/coils/16._inferred_type`: flasher
- `games/xmen.json#/coils/16._note`: SolModCallback — maps to Lampz index 125
- `games/xmen.json#/coils/17._vbscript_callback`: vpmSolDiverter RampDiverter
- `games/xmen.json#/coils/17._inferred_type`: diverter
- `games/xmen.json#/coils/18._vbscript_callback`: solIceManMotor
- `games/xmen.json#/coils/18._inferred_type`: motor
- `games/xmen.json#/coils/18._note`: Drives TimerIceManMotor for Iceman ramp rotation. LE-only feature
- `games/xmen.json#/coils/19._vbscript_callback`: SetLampMod 128
- `games/xmen.json#/coils/19._inferred_type`: flasher
- `games/xmen.json#/coils/19._note`: SolModCallback — maps to Lampz index 128
- `games/xmen.json#/coils/20._vbscript_callback`: SetLampMod 129
- `games/xmen.json#/coils/20._inferred_type`: flasher
- `games/xmen.json#/coils/20._note`: SolModCallback — maps to Lampz index 129
- `games/xmen.json#/coils/21._vbscript_callback`: SetLampMod 130
- `games/xmen.json#/coils/21._inferred_type`: flasher
- `games/xmen.json#/coils/21._note`: SolModCallback — maps to Lampz index 130
- `games/xmen.json#/coils/22._vbscript_callback`: SetLampMod 131
- `games/xmen.json#/coils/22._inferred_type`: flasher
- `games/xmen.json#/coils/22._note`: SolModCallback — maps to Lampz index 131. LE-only
- `games/xmen.json#/coils/23._vbscript_callback`: SetLampMod 132
- `games/xmen.json#/coils/23._inferred_type`: flasher
- `games/xmen.json#/coils/23._note`: SolModCallback — maps to Lampz index 132
- `games/xmen.json#/coils/24._inferred_type`: magnet
- `games/xmen.json#/coils/24._note`: cvpmMagnet on Magnet1 object, solenoid=51. Handled by cvpmMagnet.CreateEvents, no explicit SolCallback. LE-only
- `games/xmen.json#/coils/25._vbscript_callback`: solLeftNightcrawler
- `games/xmen.json#/coils/25._inferred_type`: mechanism
- `games/xmen.json#/coils/25._note`: LE-only. Moves left Nightcrawler down with shake animation
- `games/xmen.json#/coils/26._vbscript_callback`: solRightNightcrawler
- `games/xmen.json#/coils/26._inferred_type`: mechanism
- `games/xmen.json#/coils/26._note`: LE-only. Moves right Nightcrawler down with shake animation
- `games/xmen.json#/coils/27._vbscript_callback`: SolGIWhite
- `games/xmen.json#/coils/27._inferred_type`: gi
- `games/xmen.json#/coils/27._note`: SolModCallback — GI White control. Sol 44 in manual. Maps to Lampz index 100
- `games/xmen.json#/coils/28._vbscript_callback`: SolGIRed
- `games/xmen.json#/coils/28._inferred_type`: gi
- `games/xmen.json#/coils/28._note`: SolModCallback — GI Red control. Sol 45 in manual. Maps to Lampz index 101
- `games/xmen.json#/coils/29._vbscript_callback`: SolGIBlue
- `games/xmen.json#/coils/29._inferred_type`: gi
- `games/xmen.json#/coils/29._note`: SolModCallback — GI Blue control. Sol 46 in manual. Maps to Lampz index 102
- `games/xmen.json#/coils/30._vbscript_callback`: solLeftNightcrawlerLatch
- `games/xmen.json#/coils/30._inferred_type`: mechanism
- `games/xmen.json#/coils/30._note`: LE-only. When released (NOT Enabled), moves left Nightcrawler back up
- `games/xmen.json#/coils/31._vbscript_callback`: solRightNightcrawlerLatch
- `games/xmen.json#/coils/31._inferred_type`: mechanism
- `games/xmen.json#/coils/31._note`: LE-only. When released (NOT Enabled), moves right Nightcrawler back up
- `games/xmen.json#/lamps/0._inferred_type`: insert
- `games/xmen.json#/lamps/1._inferred_type`: insert
- `games/xmen.json#/lamps/2._inferred_type`: insert
- `games/xmen.json#/lamps/3._inferred_type`: insert
- `games/xmen.json#/lamps/4._inferred_type`: insert
- `games/xmen.json#/lamps/5._inferred_type`: insert
- `games/xmen.json#/lamps/6._inferred_type`: insert
- `games/xmen.json#/lamps/7._inferred_type`: insert
- `games/xmen.json#/lamps/8._inferred_type`: insert
- `games/xmen.json#/lamps/9._inferred_type`: insert
- `games/xmen.json#/lamps/10._inferred_type`: insert
- `games/xmen.json#/lamps/11._inferred_type`: insert
- `games/xmen.json#/lamps/12._inferred_type`: insert
- `games/xmen.json#/lamps/13._inferred_type`: insert
- `games/xmen.json#/lamps/14._inferred_type`: insert
- `games/xmen.json#/lamps/15._inferred_type`: insert
- `games/xmen.json#/lamps/16._inferred_type`: insert
- `games/xmen.json#/lamps/17._inferred_type`: insert
- `games/xmen.json#/lamps/18._inferred_type`: insert
- `games/xmen.json#/lamps/19._inferred_type`: insert
- `games/xmen.json#/lamps/20._inferred_type`: insert
- `games/xmen.json#/lamps/21._inferred_type`: insert
- `games/xmen.json#/lamps/22._inferred_type`: insert
- `games/xmen.json#/lamps/23._inferred_type`: insert
- `games/xmen.json#/lamps/24._inferred_type`: insert
- `games/xmen.json#/lamps/25._inferred_type`: insert
- `games/xmen.json#/lamps/26._inferred_type`: insert
- `games/xmen.json#/lamps/27._inferred_type`: insert
- `games/xmen.json#/lamps/28._inferred_type`: insert
- `games/xmen.json#/lamps/29._inferred_type`: insert
- `games/xmen.json#/lamps/30._inferred_type`: insert
- `games/xmen.json#/lamps/31._inferred_type`: insert
- `games/xmen.json#/lamps/32._inferred_type`: insert
- `games/xmen.json#/lamps/33._inferred_type`: insert
- `games/xmen.json#/lamps/34._inferred_type`: insert
- `games/xmen.json#/lamps/35._inferred_type`: insert
- `games/xmen.json#/lamps/36._inferred_type`: insert
- `games/xmen.json#/lamps/37._inferred_type`: insert
- `games/xmen.json#/lamps/38._inferred_type`: insert
- `games/xmen.json#/lamps/39._inferred_type`: insert
- `games/xmen.json#/lamps/40._inferred_type`: insert
- `games/xmen.json#/lamps/41._inferred_type`: insert
- `games/xmen.json#/lamps/42._inferred_type`: insert
- `games/xmen.json#/lamps/43._inferred_type`: insert
- `games/xmen.json#/lamps/44._inferred_type`: insert
- `games/xmen.json#/lamps/45._inferred_type`: insert
- `games/xmen.json#/lamps/46._inferred_type`: insert
- `games/xmen.json#/lamps/47._inferred_type`: insert
- `games/xmen.json#/lamps/48._inferred_type`: insert
- `games/xmen.json#/lamps/49._inferred_type`: insert
- `games/xmen.json#/lamps/50._inferred_type`: insert
- `games/xmen.json#/lamps/51._inferred_type`: insert
- `games/xmen.json#/lamps/52._inferred_type`: insert
- `games/xmen.json#/lamps/53._inferred_type`: insert
- `games/xmen.json#/lamps/54._inferred_type`: insert
- `games/xmen.json#/lamps/55._inferred_type`: insert
- `games/xmen.json#/lamps/56._inferred_type`: insert
- `games/xmen.json#/lamps/57._inferred_type`: gi
- `games/xmen.json#/lamps/57._note`: Sol 54 controls via SolGIWhite. Multiple VPX light objects (l100a-l100k)
- `games/xmen.json#/lamps/58._inferred_type`: gi
- `games/xmen.json#/lamps/58._note`: Sol 55 controls via SolGIRed. Multiple VPX light objects (l101a-l101h)
- `games/xmen.json#/lamps/59._inferred_type`: gi
- `games/xmen.json#/lamps/59._note`: Sol 56 controls via SolGIBlue. Multiple VPX light objects (l102a-l102h)
- `games/xmen.json#/lamps/60._inferred_type`: gi
- `games/xmen.json#/lamps/60._note`: Always-on base GI. VPX light objects (l103, l103b)
- `games/xmen.json#/lamps/61._inferred_type`: flasher
- `games/xmen.json#/lamps/61._note`: Driven by coil 17 via SolModCallback. VPX objects f17a, f17b
- `games/xmen.json#/lamps/62._inferred_type`: flasher
- `games/xmen.json#/lamps/62._note`: Driven by coil 18 via SolModCallback
- `games/xmen.json#/lamps/63._inferred_type`: flasher
- `games/xmen.json#/lamps/63._note`: Driven by coil 19 via SolModCallback
- `games/xmen.json#/lamps/64._inferred_type`: flasher
- `games/xmen.json#/lamps/64._note`: Driven by coil 20 via SolModCallback
- `games/xmen.json#/lamps/65._inferred_type`: flasher
- `games/xmen.json#/lamps/65._note`: Driven by coil 21 via SolModCallback
- `games/xmen.json#/lamps/66._inferred_type`: flasher
- `games/xmen.json#/lamps/66._note`: Driven by coil 22 via SolModCallback
- `games/xmen.json#/lamps/67._inferred_type`: flasher
- `games/xmen.json#/lamps/67._note`: Driven by coil 25 via SolModCallback
- `games/xmen.json#/lamps/68._inferred_type`: flasher
- `games/xmen.json#/lamps/68._note`: Driven by coil 28 via SolModCallback
- `games/xmen.json#/lamps/69._inferred_type`: flasher
- `games/xmen.json#/lamps/69._note`: Driven by coil 29 via SolModCallback
- `games/xmen.json#/lamps/70._inferred_type`: flasher
- `games/xmen.json#/lamps/70._note`: Driven by coil 30 via SolModCallback
- `games/xmen.json#/lamps/71._inferred_type`: flasher
- `games/xmen.json#/lamps/71._note`: Driven by coil 31 via SolModCallback. LE-only
- `games/xmen.json#/lamps/72._inferred_type`: flasher
- `games/xmen.json#/lamps/72._note`: Driven by coil 32 via SolModCallback
- `games/xmen.json#/_source/confidence_notes`: SAM-era Stern game (LoadVPM sam.VBS). LE variant (Wolverine & Magneto) — IPDB 5823/5824. No Const sw* definitions — all switches referenced by number via Controller.Switch(N) and vpmTimer.PulseSw N. Trough is sw18-sw21 (4-ball), manually managed via kicker objects (no cvpmTrough). Lamp IDs from Lampz.MassAssign: inserts L17-L80 high confidence, flashers 117-132 via SolModCallback, GI at 100-103 (white/red/blue/base). LE-specific features: Nightcrawler pop-ups (sol 52/53/57/58), cvpmMagnet on sol 51 (Wolverine TL magnet), Magneto magnet on sol 4 (SolModCallback), disc motor (sol 23), Iceman ramp motor (sol 27). Switches 34/35 are Iceman ramp position optos. Switch 12 is left Nightcrawler down opto, switch 56 is right Nightcrawler down opto. UseLamps=0 — ROM lamp matrix handled via Lampz framework, not core.vbs lamp handler.

## Unresolved questions

- Is the I/O enumeration complete for every supported physical/controller variant?
- Which inferred VPX behaviors reflect real hardware, and which are table-script conveniences?
- Are all mechanism home states, sensors, motion constraints, and ball interactions documented?

## Sources

- `legacy.game.xmen`: `games/xmen.json` at the pinned migration revision.
