# Monster Bash

Coverage: **partial - source-derived recreation knowledge requiring validation**

## Overview

Legacy evidence identifies this candidate as Williams (1998). The information below is preserved for recreation work but is not automatically treated as validated physical-machine fact.

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

- `platforms/wpc.json#/coils/1`: Unbound legacy outputs record `c_flipper_lower_right` was retained as a migration note only.
- `platforms/wpc.json#/coils/2`: Unbound legacy outputs record `c_flipper_lower_left` was retained as a migration note only.
- `platforms/wpc.json#/coils/3`: Unbound legacy outputs record `c_flipper_upper_right` was retained as a migration note only.
- `platforms/wpc.json#/coils/4`: Unbound legacy outputs record `c_flipper_upper_left` was retained as a migration note only.
- `games/mb.json#/switches/0._note`: Directly set via Controller.Switch(11) in KeyDown/KeyUp handlers, not a VPX object hit sub
- `games/mb.json#/switches/1._inferred_type`: standup_target
- `games/mb.json#/switches/1._note`: Uses STHit bouncer system (STArray)
- `games/mb.json#/switches/3._note`: vpmNudge.TiltSwitch = 14
- `games/mb.json#/switches/4._inferred_type`: standup_target
- `games/mb.json#/switches/4._note`: Uses STHit bouncer system (STArray)
- `games/mb.json#/switches/9._note`: Set to 1 in Table1_Init
- `games/mb.json#/switches/10._inferred_type`: standup_target
- `games/mb.json#/switches/10._note`: Uses STHit bouncer system (STArray)
- `games/mb.json#/switches/11._note`: Set to 0 in Table1_Init (Controller.Switch(24) = 0), inverted logic — normally closed opto
- `games/mb.json#/switches/12._inferred_type`: standup_target
- `games/mb.json#/switches/12._note`: Fired via vpmTimer.PulseSw 25 in DracTargets_Hit sub — rotating Dracula mechanism target
- `games/mb.json#/switches/15._inferred_type`: kicker
- `games/mb.json#/switches/16._note`: Fired via vpmTimer.PulseSw 31 in SolBallRelease
- `games/mb.json#/switches/21._inferred_type`: kicker
- `games/mb.json#/switches/24._inferred_type`: standup_target
- `games/mb.json#/switches/24._note`: Uses STHit2 bouncer system
- `games/mb.json#/switches/25._inferred_type`: standup_target
- `games/mb.json#/switches/25._note`: Uses STHit2 bouncer system
- `games/mb.json#/switches/26._inferred_type`: standup_target
- `games/mb.json#/switches/26._note`: Uses STHit2 bouncer system
- `games/mb.json#/switches/29._inferred_type`: slingshot
- `games/mb.json#/switches/29._note`: Fired via vpmTimer.PulseSw 51 in LeftSlingShot_Slingshot sub
- `games/mb.json#/switches/30._inferred_type`: slingshot
- `games/mb.json#/switches/30._note`: Fired via vpmTimer.PulseSw 52 in RightSlingShot_Slingshot sub
- `games/mb.json#/switches/31._inferred_type`: bumper
- `games/mb.json#/switches/31._note`: Fired via vpmTimer.PulseSw 53 in Bumper1_Hit
- `games/mb.json#/switches/32._inferred_type`: bumper
- `games/mb.json#/switches/32._note`: Fired via vpmTimer.PulseSw 54 in Bumper2_Hit
- `games/mb.json#/switches/33._inferred_type`: bumper
- `games/mb.json#/switches/33._note`: Fired via vpmTimer.PulseSw 55 in Bumper3_Hit
- `games/mb.json#/switches/44._note`: PulseSw — momentary pulse switch
- `games/mb.json#/switches/45._note`: PulseSw — momentary pulse switch
- `games/mb.json#/switches/48._note`: Opto — handled by controller.getmech(2), no VPX object
- `games/mb.json#/switches/49._note`: Opto — handled by controller.getmech(2), no VPX object
- `games/mb.json#/switches/50._note`: Opto — handled by controller.getmech(2), no VPX object
- `games/mb.json#/switches/51._note`: Opto — handled by controller.getmech(2), no VPX object
- `games/mb.json#/switches/52._note`: Opto — handled by controller.getmech(2), no VPX object
- `games/mb.json#/switches/53._note`: Set directly in TargetsInit and BankMove_timer. Tracks Frank target bank position.
- `games/mb.json#/switches/54._note`: Set directly in TargetsInit and BankMove_timer. Tracks Frank target bank position.
- `games/mb.json#/switches/55._note`: Set in FrankMove_timer. Tracks Frankenstein table mechanism.
- `games/mb.json#/switches/56._note`: Set in FrankInit and FrankMove_timer. Tracks Frankenstein table mechanism.
- `games/mb.json#/switches/57._inferred_type`: standup_target
- `games/mb.json#/switches/57._note`: Uses STHit bouncer system (STArray)
- `games/mb.json#/switches/58._inferred_type`: standup_target
- `games/mb.json#/switches/58._note`: Uses STHit bouncer system (STArray)
- `games/mb.json#/switches/59._note`: Set in FrankInit and FrankMove_timer. Indicates Frankenstein is in hittable position.
- `games/mb.json#/switches/60._note`: PulseSw 117 — WPC virtual switch outside 8x8 matrix, used internally by ROM
- `games/mb.json#/coils/0._vbscript_callback`: AutoPlunger
- `games/mb.json#/coils/0._inferred_type`: ball_management
- `games/mb.json#/coils/1._vbscript_callback`: SolBride
- `games/mb.json#/coils/1._inferred_type`: mechanism
- `games/mb.json#/coils/1._note`: Raises/lowers bride post (BrideH object)
- `games/mb.json#/coils/2._vbscript_callback`: SolMummy
- `games/mb.json#/coils/2._inferred_type`: mechanism
- `games/mb.json#/coils/2._note`: Opens/closes mummy coffin animation
- `games/mb.json#/coils/3._vbscript_callback`: vpmSolGate LGate,false,
- `games/mb.json#/coils/3._inferred_type`: gate
- `games/mb.json#/coils/4._vbscript_callback`: vpmSolGate Rgate,false,
- `games/mb.json#/coils/4._inferred_type`: gate
- `games/mb.json#/coils/5._vbscript_callback`: solKnocker
- `games/mb.json#/coils/5._inferred_type`: knocker
- `games/mb.json#/coils/6._vbscript_callback`: SolLockPost
- `games/mb.json#/coils/6._inferred_type`: mechanism
- `games/mb.json#/coils/6._note`: Raises/lowers ramp lock post (lock object)
- `games/mb.json#/coils/7._vbscript_callback`: SolBallRelease
- `games/mb.json#/coils/7._inferred_type`: ball_management
- `games/mb.json#/coils/7._note`: Kicks ball from sw32 (trough ball 1)
- `games/mb.json#/coils/8._inferred_type`: slingshot
- `games/mb.json#/coils/8._note`: SolCallback commented out in script but ROM still fires it
- `games/mb.json#/coils/9._inferred_type`: slingshot
- `games/mb.json#/coils/9._note`: SolCallback commented out in script but ROM still fires it
- `games/mb.json#/coils/10._inferred_type`: bumper
- `games/mb.json#/coils/10._note`: SolCallback commented out in script but ROM still fires it
- `games/mb.json#/coils/11._inferred_type`: bumper
- `games/mb.json#/coils/11._note`: SolCallback commented out in script but ROM still fires it
- `games/mb.json#/coils/12._inferred_type`: bumper
- `games/mb.json#/coils/12._note`: SolCallback commented out in script but ROM still fires it
- `games/mb.json#/coils/13._vbscript_callback`: SolSaucer
- `games/mb.json#/coils/13._inferred_type`: kicker
- `games/mb.json#/coils/14._vbscript_callback`: SolRightScoop
- `games/mb.json#/coils/14._inferred_type`: kicker
- `games/mb.json#/coils/15._vbscript_callback`: SetModLamp 117,
- `games/mb.json#/coils/15._inferred_type`: flasher
- `games/mb.json#/coils/16._vbscript_callback`: SetModLamp 118,
- `games/mb.json#/coils/16._inferred_type`: flasher
- `games/mb.json#/coils/17._vbscript_callback`: Flashsol19
- `games/mb.json#/coils/17._inferred_type`: flasher
- `games/mb.json#/coils/17._note`: Uses custom flupper dome flasher system
- `games/mb.json#/coils/18._vbscript_callback`: SetModLamp 120,
- `games/mb.json#/coils/18._inferred_type`: flasher
- `games/mb.json#/coils/19._vbscript_callback`: SolCreature
- `games/mb.json#/coils/19._inferred_type`: flasher
- `games/mb.json#/coils/19._note`: Also controls Creature animation — SetModLamp 121 + creature shake mechanism
- `games/mb.json#/coils/20._vbscript_callback`: SetModLamp 122,
- `games/mb.json#/coils/20._inferred_type`: flasher
- `games/mb.json#/coils/21._vbscript_callback`: FlashSol23
- `games/mb.json#/coils/21._inferred_type`: flasher
- `games/mb.json#/coils/21._note`: Uses custom flupper dome flasher system
- `games/mb.json#/coils/22._vbscript_callback`: SetModLamp 124,
- `games/mb.json#/coils/22._inferred_type`: flasher
- `games/mb.json#/coils/23._vbscript_callback`: SetModLamp 125,
- `games/mb.json#/coils/23._inferred_type`: flasher
- `games/mb.json#/coils/24._vbscript_callback`: SetLamp 126,
- `games/mb.json#/coils/24._inferred_type`: flasher
- `games/mb.json#/coils/25._vbscript_callback`: SolFrank
- `games/mb.json#/coils/25._inferred_type`: mechanism
- `games/mb.json#/coils/25._note`: Drives Frankenstein body up/down animation
- `games/mb.json#/coils/26._vbscript_callback`: SolBank
- `games/mb.json#/coils/26._inferred_type`: mechanism
- `games/mb.json#/coils/26._note`: Drives Frank target bank up/down movement
- `games/mb.json#/coils/27._vbscript_callback`: SolDrac
- `games/mb.json#/coils/27._inferred_type`: mechanism
- `games/mb.json#/coils/27._note`: Drives Dracula rotating coffin mechanism. Uses controller.getmech(2) for position.
- `games/mb.json#/lamps/0._note`: Multiple VPX objects: l11, l11a, l11halo
- `games/mb.json#/lamps/1._note`: Multiple VPX objects: l12c, l12
- `games/mb.json#/lamps/2._note`: Multiple VPX objects: l13, l13halo
- `games/mb.json#/lamps/3._note`: Multiple VPX objects: l14, l14halo
- `games/mb.json#/lamps/4._note`: Multiple VPX objects: l15, l15halo
- `games/mb.json#/lamps/5._note`: Multiple VPX objects: l16, l16halo
- `games/mb.json#/lamps/6._note`: Multiple VPX objects: l17, l17halo
- `games/mb.json#/lamps/7._note`: Multiple VPX objects: l18, l18halo
- `games/mb.json#/lamps/8._note`: Multiple VPX objects: l21, l21halo
- `games/mb.json#/lamps/9._note`: Multiple VPX objects: l22, l22halo
- `games/mb.json#/lamps/11._note`: Multiple VPX objects: l24c, l24, l24halo, l24chalo
- `games/mb.json#/lamps/12._note`: Multiple VPX objects: l25, l25halo
- `games/mb.json#/lamps/13._note`: Multiple VPX objects: l26, l26halo
- `games/mb.json#/lamps/14._note`: Multiple VPX objects: l27, l27halo
- `games/mb.json#/lamps/15._note`: Multiple VPX objects: l28, l28halo
- `games/mb.json#/lamps/16._note`: Multiple VPX objects: l31c, l31
- `games/mb.json#/lamps/17._note`: Multiple VPX objects: l32, l32halo
- `games/mb.json#/lamps/19._note`: Multiple VPX objects: l34, l34halo
- `games/mb.json#/lamps/23._note`: Multiple VPX objects: l38, l38halo
- `games/mb.json#/lamps/25._note`: Multiple VPX objects: l42, l42halo
- `games/mb.json#/lamps/26._note`: Multiple VPX objects: l43c, l43
- `games/mb.json#/lamps/27._note`: Multiple VPX objects: l44, l44halo
- `games/mb.json#/lamps/28._note`: Multiple VPX objects: l45, l45halo
- `games/mb.json#/lamps/29._note`: Multiple VPX objects: l46, l46halo
- `games/mb.json#/lamps/30._note`: Multiple VPX objects: l47, l47halo
- `games/mb.json#/lamps/31._note`: Multiple VPX objects: l48, l48halo
- `games/mb.json#/lamps/38._note`: Multiple VPX objects: l57, l57a, l57halo
- `games/mb.json#/lamps/39._note`: Multiple VPX objects: l58, l58halo
- `games/mb.json#/lamps/40._note`: Multiple VPX objects: l61, l61a
- `games/mb.json#/lamps/41._note`: Multiple VPX objects: l62, l62a
- `games/mb.json#/lamps/42._note`: Multiple VPX objects: l63, l63a
- `games/mb.json#/lamps/43._note`: Multiple VPX objects: l64, l64a
- `games/mb.json#/lamps/44._note`: Multiple VPX objects: l65, l65a
- `games/mb.json#/lamps/45._note`: Multiple VPX objects: l66, l66a
- `games/mb.json#/lamps/46._note`: Multiple VPX objects: l67, l67halo
- `games/mb.json#/lamps/47._note`: Multiple VPX objects: l68, l68halo
- `games/mb.json#/lamps/50._note`: Multiple VPX objects: l73, l73halo
- `games/mb.json#/lamps/54._note`: Multiple VPX objects: l77, l77halo
- `games/mb.json#/lamps/55._note`: Monster feature lamp. Multiple VPX objects: l81pp, l81pp2, l81f, l81f2, l81ref
- `games/mb.json#/lamps/56._note`: Monster feature lamp. Multiple VPX objects: l82pp, l82pp2, l82f, l82f2, l82ref
- `games/mb.json#/lamps/57._note`: Monster feature lamp. Multiple VPX objects: l83pp, l83pp2, l83f, l83f2
- `games/mb.json#/lamps/58._note`: Monster feature lamp. Multiple VPX objects: l84pp, l84pp2, l84f, l84f2
- `games/mb.json#/lamps/59._note`: Multiple VPX objects: l85, l85a, l85halo
- `games/mb.json#/lamps/60._note`: Multiple VPX objects: l86, l86a, l86halo
- `games/mb.json#/_source/confidence_notes`: High confidence on switches/coils from VBScript hit/unhit subs and SolCallback assignments. Lamp IDs from UpdateLamps NFadeL/NFadeLm calls. Flasher coils (17-26) use SolModCallback with SetModLamp/flasher routines. Dracula position switches (74-78) are opto-based and handled by controller.getmech(2), not direct VPX objects. Spinner (sw117) fires PulseSw 117 but 117 is outside the 8x8 matrix — this is a WPC virtual switch used internally. Commented-out SolCallbacks for slingshots (10-11) and bumpers (12-14) included as coils since the ROM still fires them.

## Unresolved questions

- Is the I/O enumeration complete for every supported physical/controller variant?
- Which inferred VPX behaviors reflect real hardware, and which are table-script conveniences?
- Are all mechanism home states, sensors, motion constraints, and ball interactions documented?

## Sources

- `legacy.game.mb`: `games/mb.json` at the pinned migration revision.
