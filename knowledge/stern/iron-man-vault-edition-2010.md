# Iron Man Vault Edition

Coverage: **partial - source-derived recreation knowledge requiring validation**

## Overview

Legacy evidence identifies this candidate as Stern (2010). The information below is preserved for recreation work but is not automatically treated as validated physical-machine fact.

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
- `games/ironman.json#/switches/0._inferred_type`: opto
- `games/ironman.json#/switches/0._note`: Set programmatically by Solmonger sub when monger closes (Controller.Switch(1)=1)
- `games/ironman.json#/switches/1._inferred_type`: opto
- `games/ironman.json#/switches/1._note`: Set programmatically by Solmonger sub when monger opens (Controller.Switch(3)=1)
- `games/ironman.json#/switches/2._inferred_type`: standup_target
- `games/ironman.json#/switches/2._note`: Target on Iron Monger toy, PulseSw. IsDropped when monger closed.
- `games/ironman.json#/switches/3._inferred_type`: standup_target
- `games/ironman.json#/switches/3._note`: Target on Iron Monger toy, PulseSw. IsDropped when monger closed.
- `games/ironman.json#/switches/4._inferred_type`: standup_target
- `games/ironman.json#/switches/4._note`: Target on Iron Monger toy, PulseSw. IsDropped when monger closed.
- `games/ironman.json#/switches/5._inferred_type`: rollover
- `games/ironman.json#/switches/5._note`: Has Update_Wires + Controller.Switch
- `games/ironman.json#/switches/6._inferred_type`: rollover
- `games/ironman.json#/switches/6._note`: Has Update_Wires + Controller.Switch
- `games/ironman.json#/switches/7._inferred_type`: kicker
- `games/ironman.json#/switches/7._note`: Ball captured on hit, ejected by sol 5 (WMKick)
- `games/ironman.json#/switches/8._inferred_type`: spinner
- `games/ironman.json#/switches/8._note`: sw11_Spin PulseSw 11
- `games/ironman.json#/switches/9._inferred_type`: rollover
- `games/ironman.json#/switches/9._note`: Controller.Switch hit/unhit
- `games/ironman.json#/switches/10._inferred_type`: spinner
- `games/ironman.json#/switches/10._note`: sw13_Spin PulseSw 13
- `games/ironman.json#/switches/11._inferred_type`: spinner
- `games/ironman.json#/switches/11._note`: sw14_Spin PulseSw 14
- `games/ironman.json#/switches/12._inferred_type`: pulse
- `games/ironman.json#/switches/12._note`: PulseSw 15 fired during SolRelease — ball eject confirmation
- `games/ironman.json#/switches/13._inferred_type`: cabinet
- `games/ironman.json#/switches/13._note`: Set via Table_KeyDown/Up StartGameKey
- `games/ironman.json#/switches/14._inferred_type`: trough
- `games/ironman.json#/switches/15._inferred_type`: trough
- `games/ironman.json#/switches/16._inferred_type`: trough
- `games/ironman.json#/switches/17._inferred_type`: trough
- `games/ironman.json#/switches/18._inferred_type`: rollover
- `games/ironman.json#/switches/19._inferred_type`: rollover
- `games/ironman.json#/switches/19._note`: Has Update_Wires + Controller.Switch
- `games/ironman.json#/switches/20._inferred_type`: rollover
- `games/ironman.json#/switches/20._note`: Has Update_Wires + Controller.Switch
- `games/ironman.json#/switches/21._inferred_type`: slingshot
- `games/ironman.json#/switches/21._note`: PulseSw 26 via LeftSlingShot_Slingshot
- `games/ironman.json#/switches/22._inferred_type`: slingshot
- `games/ironman.json#/switches/22._note`: PulseSw 27 via RightSlingShot_Slingshot
- `games/ironman.json#/switches/23._inferred_type`: rollover
- `games/ironman.json#/switches/23._note`: Has Update_Wires + Controller.Switch
- `games/ironman.json#/switches/24._inferred_type`: rollover
- `games/ironman.json#/switches/24._note`: Has Update_Wires + Controller.Switch
- `games/ironman.json#/switches/25._inferred_type`: bumper
- `games/ironman.json#/switches/25._note`: PulseSw 30 via Bumper1_Hit
- `games/ironman.json#/switches/26._inferred_type`: bumper
- `games/ironman.json#/switches/26._note`: PulseSw 31 via Bumper2_Hit
- `games/ironman.json#/switches/27._inferred_type`: bumper
- `games/ironman.json#/switches/27._note`: PulseSw 32 via Bumper3_Hit
- `games/ironman.json#/switches/28._inferred_type`: standup_target
- `games/ironman.json#/switches/28._note`: STHit framework target
- `games/ironman.json#/switches/29._inferred_type`: standup_target
- `games/ironman.json#/switches/29._note`: STHit framework target
- `games/ironman.json#/switches/30._inferred_type`: standup_target
- `games/ironman.json#/switches/30._note`: STHit framework target
- `games/ironman.json#/switches/31._inferred_type`: standup_target
- `games/ironman.json#/switches/31._note`: STHit framework target
- `games/ironman.json#/switches/32._inferred_type`: rollover
- `games/ironman.json#/switches/32._note`: Controller.Switch hit/unhit
- `games/ironman.json#/switches/33._inferred_type`: rollover
- `games/ironman.json#/switches/33._note`: Has Update_Wires + Controller.Switch
- `games/ironman.json#/switches/34._inferred_type`: rollover
- `games/ironman.json#/switches/34._note`: Has Update_Wires + Controller.Switch
- `games/ironman.json#/switches/35._inferred_type`: standup_target
- `games/ironman.json#/switches/35._note`: STHit framework target
- `games/ironman.json#/switches/36._inferred_type`: standup_target
- `games/ironman.json#/switches/36._note`: STHit framework target
- `games/ironman.json#/switches/37._inferred_type`: standup_target
- `games/ironman.json#/switches/37._note`: STHit framework target
- `games/ironman.json#/switches/38._inferred_type`: rollover
- `games/ironman.json#/switches/38._note`: Controller.Switch hit/unhit
- `games/ironman.json#/switches/39._inferred_type`: standup_target
- `games/ironman.json#/switches/39._note`: STHit framework target
- `games/ironman.json#/switches/40._inferred_type`: standup_target
- `games/ironman.json#/switches/40._note`: STHit framework target
- `games/ironman.json#/switches/41._inferred_type`: standup_target
- `games/ironman.json#/switches/41._note`: STHit framework target
- `games/ironman.json#/switches/42._inferred_type`: standup_target
- `games/ironman.json#/switches/42._note`: STHit framework target
- `games/ironman.json#/switches/43._inferred_type`: standup_target
- `games/ironman.json#/switches/43._note`: STHit framework target
- `games/ironman.json#/switches/44._inferred_type`: rollover
- `games/ironman.json#/switches/44._note`: Controller.Switch hit/unhit
- `games/ironman.json#/switches/45._inferred_type`: standup_target
- `games/ironman.json#/switches/45._note`: STHit framework target
- `games/ironman.json#/switches/46._inferred_type`: cabinet
- `games/ironman.json#/switches/46._note`: vpmNudge.TiltSwitch=-7 (negative = virtual slam tilt)
- `games/ironman.json#/coils/0._vbscript_callback`: SolRelease
- `games/ironman.json#/coils/0._inferred_type`: ball_management
- `games/ironman.json#/coils/0._note`: Kicks from sw21, pulses sw15 on release
- `games/ironman.json#/coils/1._vbscript_callback`: solAutofire
- `games/ironman.json#/coils/1._inferred_type`: ball_management
- `games/ironman.json#/coils/1._note`: Impulse plunger auto-fire
- `games/ironman.json#/coils/2._inferred_type`: magnet
- `games/ironman.json#/coils/2._note`: cvpmMagnet mag1, solenoid=3, size=50
- `games/ironman.json#/coils/3._inferred_type`: magnet
- `games/ironman.json#/coils/3._note`: cvpmMagnet mag2, solenoid=4, size=30
- `games/ironman.json#/coils/4._vbscript_callback`: WMKick
- `games/ironman.json#/coils/4._inferred_type`: kicker
- `games/ironman.json#/coils/4._note`: Kicks ball from sw10 kicker
- `games/ironman.json#/coils/5._vbscript_callback`: orbitpost
- `games/ironman.json#/coils/5._inferred_type`: mechanism
- `games/ironman.json#/coils/5._note`: Raises/lowers orbit lane diverter post
- `games/ironman.json#/coils/6._vbscript_callback`: ClanePost
- `games/ironman.json#/coils/6._inferred_type`: mechanism
- `games/ironman.json#/coils/6._note`: Raises/lowers center lane diverter post
- `games/ironman.json#/coils/7._vbscript_callback`: SolLFlipper
- `games/ironman.json#/coils/7._inferred_type`: flipper
- `games/ironman.json#/coils/8._vbscript_callback`: SolRFlipper
- `games/ironman.json#/coils/8._inferred_type`: flipper
- `games/ironman.json#/coils/9._vbscript_callback`: Solmonger
- `games/ironman.json#/coils/9._inferred_type`: mechanism
- `games/ironman.json#/coils/9._note`: Toggles Iron Monger toy up/down. Sets sw1 (down) and sw3 (up) programmatically.
- `games/ironman.json#/coils/10._vbscript_callback`: SetLampMod 120
- `games/ironman.json#/coils/10._inferred_type`: flasher
- `games/ironman.json#/coils/10._note`: SolModCallback — modulated flasher mapped to Lampz 120
- `games/ironman.json#/coils/11._vbscript_callback`: SetLampMod 121
- `games/ironman.json#/coils/11._inferred_type`: flasher
- `games/ironman.json#/coils/11._note`: SolModCallback — modulated flasher mapped to Lampz 121
- `games/ironman.json#/coils/12._vbscript_callback`: SetLampMod 122
- `games/ironman.json#/coils/12._inferred_type`: flasher
- `games/ironman.json#/coils/12._note`: SolModCallback — modulated flasher mapped to Lampz 122
- `games/ironman.json#/coils/13._vbscript_callback`: SetLampMod 123
- `games/ironman.json#/coils/13._inferred_type`: flasher
- `games/ironman.json#/coils/13._note`: SolModCallback — modulated flasher mapped to Lampz 123
- `games/ironman.json#/coils/14._vbscript_callback`: SetLampMod 124
- `games/ironman.json#/coils/14._inferred_type`: flasher
- `games/ironman.json#/coils/14._note`: SolModCallback — modulated flasher mapped to Lampz 124. No VPX light assigned.
- `games/ironman.json#/coils/15._vbscript_callback`: SetLampMod 125
- `games/ironman.json#/coils/15._inferred_type`: flasher
- `games/ironman.json#/coils/15._note`: SolModCallback — modulated flasher mapped to Lampz 125
- `games/ironman.json#/coils/16._vbscript_callback`: SetLampMod 126
- `games/ironman.json#/coils/16._inferred_type`: flasher
- `games/ironman.json#/coils/16._note`: SolModCallback — modulated flasher mapped to Lampz 126
- `games/ironman.json#/coils/17._vbscript_callback`: SetLampMod 127
- `games/ironman.json#/coils/17._inferred_type`: flasher
- `games/ironman.json#/coils/17._note`: SolModCallback — modulated flasher mapped to Lampz 127 (l127a, l127b)
- `games/ironman.json#/coils/18._vbscript_callback`: SetLampMod 128
- `games/ironman.json#/coils/18._inferred_type`: flasher
- `games/ironman.json#/coils/18._note`: SolModCallback — modulated flasher mapped to Lampz 128
- `games/ironman.json#/coils/19._vbscript_callback`: SetLampMod 129
- `games/ironman.json#/coils/19._inferred_type`: flasher
- `games/ironman.json#/coils/19._note`: SolModCallback — modulated flasher mapped to Lampz 129
- `games/ironman.json#/coils/20._vbscript_callback`: SetLampMod 130
- `games/ironman.json#/coils/20._inferred_type`: flasher
- `games/ironman.json#/coils/20._note`: SolModCallback — modulated flasher mapped to Lampz 130
- `games/ironman.json#/coils/21._vbscript_callback`: SetLampMod 131
- `games/ironman.json#/coils/21._inferred_type`: flasher
- `games/ironman.json#/coils/21._note`: SolModCallback — modulated flasher mapped to Lampz 131
- `games/ironman.json#/coils/22._vbscript_callback`: SetLampMod 132
- `games/ironman.json#/coils/22._inferred_type`: flasher
- `games/ironman.json#/coils/22._note`: SolModCallback — modulated flasher mapped to Lampz 132
- `games/ironman.json#/lamps/0._note`: Commented out MassAssign; callback drives VR_StartButtInner
- `games/ironman.json#/lamps/1._note`: Commented out MassAssign; callback drives VR_TourneyButt
- `games/ironman.json#/lamps/2._inferred_type`: insert
- `games/ironman.json#/lamps/3._inferred_type`: insert
- `games/ironman.json#/lamps/4._inferred_type`: insert
- `games/ironman.json#/lamps/5._inferred_type`: insert
- `games/ironman.json#/lamps/6._inferred_type`: insert
- `games/ironman.json#/lamps/7._inferred_type`: insert
- `games/ironman.json#/lamps/8._inferred_type`: insert
- `games/ironman.json#/lamps/9._inferred_type`: insert
- `games/ironman.json#/lamps/10._inferred_type`: insert
- `games/ironman.json#/lamps/11._inferred_type`: insert
- `games/ironman.json#/lamps/12._inferred_type`: insert
- `games/ironman.json#/lamps/13._inferred_type`: insert
- `games/ironman.json#/lamps/14._inferred_type`: insert
- `games/ironman.json#/lamps/15._inferred_type`: insert
- `games/ironman.json#/lamps/16._inferred_type`: insert
- `games/ironman.json#/lamps/17._inferred_type`: insert
- `games/ironman.json#/lamps/18._inferred_type`: insert
- `games/ironman.json#/lamps/19._inferred_type`: insert
- `games/ironman.json#/lamps/20._inferred_type`: insert
- `games/ironman.json#/lamps/21._inferred_type`: insert
- `games/ironman.json#/lamps/22._inferred_type`: insert
- `games/ironman.json#/lamps/23._inferred_type`: insert
- `games/ironman.json#/lamps/24._inferred_type`: insert
- `games/ironman.json#/lamps/25._inferred_type`: insert
- `games/ironman.json#/lamps/26._inferred_type`: insert
- `games/ironman.json#/lamps/27._inferred_type`: insert
- `games/ironman.json#/lamps/28._inferred_type`: insert
- `games/ironman.json#/lamps/29._inferred_type`: insert
- `games/ironman.json#/lamps/30._inferred_type`: insert
- `games/ironman.json#/lamps/31._inferred_type`: insert
- `games/ironman.json#/lamps/32._inferred_type`: insert
- `games/ironman.json#/lamps/33._inferred_type`: insert
- `games/ironman.json#/lamps/34._inferred_type`: insert
- `games/ironman.json#/lamps/35._inferred_type`: insert
- `games/ironman.json#/lamps/36._inferred_type`: insert
- `games/ironman.json#/lamps/37._inferred_type`: insert
- `games/ironman.json#/lamps/38._inferred_type`: insert
- `games/ironman.json#/lamps/39._inferred_type`: insert
- `games/ironman.json#/lamps/40._inferred_type`: insert
- `games/ironman.json#/lamps/41._inferred_type`: insert
- `games/ironman.json#/lamps/42._inferred_type`: insert
- `games/ironman.json#/lamps/43._inferred_type`: insert
- `games/ironman.json#/lamps/44._inferred_type`: insert
- `games/ironman.json#/lamps/45._inferred_type`: insert
- `games/ironman.json#/lamps/46._inferred_type`: insert
- `games/ironman.json#/lamps/47._inferred_type`: insert
- `games/ironman.json#/lamps/48._inferred_type`: insert
- `games/ironman.json#/lamps/49._inferred_type`: insert
- `games/ironman.json#/lamps/50._inferred_type`: insert
- `games/ironman.json#/lamps/51._inferred_type`: insert
- `games/ironman.json#/lamps/52._inferred_type`: insert
- `games/ironman.json#/lamps/53._inferred_type`: insert
- `games/ironman.json#/lamps/54._inferred_type`: insert
- `games/ironman.json#/lamps/55._inferred_type`: insert
- `games/ironman.json#/lamps/56._inferred_type`: insert
- `games/ironman.json#/lamps/57._inferred_type`: insert
- `games/ironman.json#/lamps/58._inferred_type`: insert
- `games/ironman.json#/lamps/59._inferred_type`: insert
- `games/ironman.json#/lamps/60._inferred_type`: insert
- `games/ironman.json#/lamps/61._inferred_type`: insert
- `games/ironman.json#/lamps/62._inferred_type`: insert
- `games/ironman.json#/lamps/63._inferred_type`: gi
- `games/ironman.json#/lamps/63._note`: Lampz index 104, drives GILights collection
- `games/ironman.json#/lamps/64._inferred_type`: flasher
- `games/ironman.json#/lamps/64._note`: Driven by SolModCallback coil 20
- `games/ironman.json#/lamps/65._inferred_type`: flasher
- `games/ironman.json#/lamps/65._note`: Driven by SolModCallback coil 21
- `games/ironman.json#/lamps/66._inferred_type`: flasher
- `games/ironman.json#/lamps/66._note`: Driven by SolModCallback coil 22
- `games/ironman.json#/lamps/67._inferred_type`: flasher
- `games/ironman.json#/lamps/67._note`: Driven by SolModCallback coil 23
- `games/ironman.json#/lamps/68._inferred_type`: flasher
- `games/ironman.json#/lamps/68._note`: Driven by SolModCallback coil 25
- `games/ironman.json#/lamps/69._inferred_type`: flasher
- `games/ironman.json#/lamps/69._note`: Driven by SolModCallback coil 26
- `games/ironman.json#/lamps/70._inferred_type`: flasher
- `games/ironman.json#/lamps/70._note`: Driven by SolModCallback coil 27. Two VPX lights: l127a, l127b.
- `games/ironman.json#/lamps/71._inferred_type`: flasher
- `games/ironman.json#/lamps/71._note`: Driven by SolModCallback coil 28. MassAssign commented out — callback only.
- `games/ironman.json#/lamps/72._inferred_type`: flasher
- `games/ironman.json#/lamps/72._note`: Driven by SolModCallback coil 29. MassAssign commented out — callback only.
- `games/ironman.json#/lamps/73._inferred_type`: flasher
- `games/ironman.json#/lamps/73._note`: Driven by SolModCallback coil 30
- `games/ironman.json#/lamps/74._inferred_type`: flasher
- `games/ironman.json#/lamps/74._note`: Driven by SolModCallback coil 31
- `games/ironman.json#/lamps/75._inferred_type`: flasher
- `games/ironman.json#/lamps/75._note`: Driven by SolModCallback coil 32
- `games/ironman.json#/lamps/76._inferred_type`: gi
- `games/ironman.json#/lamps/76._note`: Virtual room ambient lighting. Lampz.Callback only (MassAssign commented out).
- `games/ironman.json#/_source/confidence_notes`: SAM-era Stern game with UseVPMModSol=True. No Const sw* definitions — switches referenced by number via Controller.Switch(N) and vpmTimer.PulseSw N. Trough is custom (4-ball, sw18-sw21 with manual cascade logic, not cvpmTrough). Iron Monger toy uses sol 19 with position switches 1 (down) and 3 (up) set programmatically. Magnets on sol 3 and 4. Flashers driven by SolModCallback (coils 20-32) mapped to Lampz indexes 120-132. GI at Lampz index 104. Lamp 150 is room lighting (virtual). Commented-out switch subs replaced by STHit standup target framework. swplunger VPX object used for impulse plunger via cvpmImpulseP — Update_Wires calls are physics-only, not ROM switch assignments.

## Unresolved questions

- Is the I/O enumeration complete for every supported physical/controller variant?
- Which inferred VPX behaviors reflect real hardware, and which are table-script conveniences?
- Are all mechanism home states, sensors, motion constraints, and ball interactions documented?

## Sources

- `legacy.game.ironman`: `games/ironman.json` at the pinned migration revision.
