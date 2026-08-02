# Congo

Coverage: **partial - source-derived recreation knowledge requiring validation**

## Overview

Legacy evidence identifies this candidate as Williams (1995). The information below is preserved for recreation work but is not automatically treated as validated physical-machine fact.

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
- `games/congo.json#/switches/0._note`: Controller.Switch(11) on/off via sw11_Hit/UnHit
- `games/congo.json#/switches/1._note`: Controller.Switch(12) on/off via sw12_Hit/UnHit. Comment says 'Volcano Switch'
- `games/congo.json#/switches/2._note`: vpmNudge.TiltSwitch = 14
- `games/congo.json#/switches/3._note`: Controller.Switch(15) on/off via sw15_Hit/UnHit
- `games/congo.json#/switches/4._note`: Controller.Switch(16) on/off. Comment: 'Kickback'
- `games/congo.json#/switches/5._note`: Controller.Switch(17) on/off
- `games/congo.json#/switches/6._note`: Controller.Switch(18) on/off. Comment: 'Shooter Lane'
- `games/congo.json#/switches/7._note`: Controller.Switch(22) = 1 set in Table1_Init. Not a VPX object.
- `games/congo.json#/switches/8._note`: Controller.Switch(24) = 1 set in Table1_Init. Not a VPX object.
- `games/congo.json#/switches/9._note`: PulseSw 25. Comment: 'Right Eject Rubber'
- `games/congo.json#/switches/10._note`: Controller.Switch(26) on/off
- `games/congo.json#/switches/11._note`: Controller.Switch(27) on/off
- `games/congo.json#/switches/12._note`: PulseSw 28 with TargetBouncer. Part of 'We Are Watching You' targets.
- `games/congo.json#/switches/13._note`: PulseSw 31 fired in SolRelease callback when trough ejects. Not a VPX object — virtual switch.
- `games/congo.json#/switches/14._note`: bsTrough.initSwitches Array(32, 33, 34, 35). First in array = closest to drain.
- `games/congo.json#/switches/15._note`: bsTrough.initSwitches Array(32, 33, 34, 35)
- `games/congo.json#/switches/16._note`: bsTrough.initSwitches Array(32, 33, 34, 35)
- `games/congo.json#/switches/17._note`: bsTrough.initSwitches Array(32, 33, 34, 35). Last in array = closest to eject.
- `games/congo.json#/switches/18._note`: PulseSw 36 via Sw36_Hit. Ball added to bsVolcano.
- `games/congo.json#/switches/19._note`: Controller.Switch(37) = 1. Ball added to bsMystery.
- `games/congo.json#/switches/20._note`: Controller.Switch(38) = 1. Ball added to bsMap.
- `games/congo.json#/switches/21._note`: bsVolcano.initSwitches Array(41, 42, 43). Volcano is a separate cvpmTrough with 3 switches.
- `games/congo.json#/switches/22._note`: bsVolcano.initSwitches Array(41, 42, 43)
- `games/congo.json#/switches/23._note`: bsVolcano.initSwitches Array(41, 42, 43)
- `games/congo.json#/switches/24._note`: Controller.Switch(44) on/off via sw44_Hit/UnHit
- `games/congo.json#/switches/25._note`: Controller.Switch(45) on/off via sw45_Hit/UnHit
- `games/congo.json#/switches/26._note`: PulseSw 46 with TargetBouncer
- `games/congo.json#/switches/27._note`: PulseSw 47 with TargetBouncer
- `games/congo.json#/switches/28._note`: PulseSw 48 with TargetBouncer
- `games/congo.json#/switches/29._note`: PulseSw 51 with TargetBouncer
- `games/congo.json#/switches/30._note`: PulseSw 52 with TargetBouncer
- `games/congo.json#/switches/31._note`: Controller.Switch(53) = 1 in sw53_hit. Ball added to bsAmyVuk (cvpmSaucer).
- `games/congo.json#/switches/32._note`: PulseSw 54 with TargetBouncer. Comment: 'We Are'
- `games/congo.json#/switches/33._note`: PulseSw 55 with TargetBouncer. Comment: 'Watching'
- `games/congo.json#/switches/34._note`: PulseSw 56 with TargetBouncer. Comment: 'Laser Perimeter'
- `games/congo.json#/switches/35._note`: Controller.Switch(57) on/off
- `games/congo.json#/switches/36._note`: Controller.Switch(58) on/off
- `games/congo.json#/switches/37._note`: PulseSw 61 in LeftSlingShot_Slingshot sub
- `games/congo.json#/switches/38._note`: PulseSw 62 in RightSlingShot_Slingshot sub
- `games/congo.json#/switches/39._note`: PulseSw 63 in Bumper1_Hit
- `games/congo.json#/switches/40._note`: PulseSw 64 in Bumper2_Hit
- `games/congo.json#/switches/41._note`: PulseSw 65 in Bumper3_Hit
- `games/congo.json#/switches/42._note`: Controller.Switch(67) on/off
- `games/congo.json#/switches/43._note`: Controller.Switch(68) on/off
- `games/congo.json#/switches/44._note`: Controller.Switch(71) on/off. Comment: 'AMY Rollovers'
- `games/congo.json#/switches/45._note`: Controller.Switch(72) on/off. Comment: 'AMY Rollovers'
- `games/congo.json#/switches/46._note`: Controller.Switch(73) on/off. Comment: 'AMY Rollovers'
- `games/congo.json#/switches/47._note`: PulseSw 74
- `games/congo.json#/switches/48._note`: PulseSw 75
- `games/congo.json#/switches/49._note`: PulseSw 76
- `games/congo.json#/switches/50._note`: PulseSw 77
- `games/congo.json#/switches/51._note`: PulseSw 78
- `games/congo.json#/coils/0._vbscript_callback`: Auto_Plunger
- `games/congo.json#/coils/0._inferred_type`: ball_management
- `games/congo.json#/coils/0._note`: Fires AutoPlunger kicker. Plays release sound.
- `games/congo.json#/coils/1._vbscript_callback`: Kick_back
- `games/congo.json#/coils/1._inferred_type`: ball_management
- `games/congo.json#/coils/1._note`: Fires KickBack kicker from left outlane.
- `games/congo.json#/coils/2._vbscript_callback`: SolPopUp
- `games/congo.json#/coils/2._inferred_type`: ball_management
- `games/congo.json#/coils/2._note`: Ejects ball from bsAmyVuk (cvpmSaucer at sw53) upward via SolOutAlt 0.
- `games/congo.json#/coils/3._vbscript_callback`: SolPopDown
- `games/congo.json#/coils/3._inferred_type`: ball_management
- `games/congo.json#/coils/3._note`: Ejects ball from bsAmyVuk downward via SolOutAlt 1.
- `games/congo.json#/coils/4._vbscript_callback`: RampDiverter
- `games/congo.json#/coils/4._inferred_type`: diverter
- `games/congo.json#/coils/4._note`: Rotates Diverter object, drops/raises DiverterSwoop.
- `games/congo.json#/coils/5._vbscript_callback`: VolcanoKickOut
- `games/congo.json#/coils/5._inferred_type`: ball_management
- `games/congo.json#/coils/5._note`: Ejects from bsVolcano (cvpmTrough, exit via sw36a kicker).
- `games/congo.json#/coils/6._vbscript_callback`: vpmSolSound SoundFX("Knocker",DOFKnocker),
- `games/congo.json#/coils/6._inferred_type`: knocker
- `games/congo.json#/coils/7._vbscript_callback`: SolTopPost
- `games/congo.json#/coils/7._inferred_type`: mechanism
- `games/congo.json#/coils/7._note`: Drops/raises TopPost. Used for ball lock mechanism.
- `games/congo.json#/coils/8._vbscript_callback`: SolRelease
- `games/congo.json#/coils/8._inferred_type`: ball_management
- `games/congo.json#/coils/8._note`: Ejects from bsTrough via BallRelease kicker. Also fires PulseSw 31.
- `games/congo.json#/coils/9._vbscript_callback`: GorillaRight
- `games/congo.json#/coils/9._inferred_type`: mechanism
- `games/congo.json#/coils/9._note`: Rotates gorilla animatronic right. Drives GorDest/GorDirection for physics animation.
- `games/congo.json#/coils/10._vbscript_callback`: GorillaLeft
- `games/congo.json#/coils/10._inferred_type`: mechanism
- `games/congo.json#/coils/10._note`: Rotates gorilla animatronic left. Drives GorDest/GorDirection for physics animation.
- `games/congo.json#/coils/11._vbscript_callback`: SolFlash17
- `games/congo.json#/coils/11._inferred_type`: flasher
- `games/congo.json#/coils/11._note`: SolModCallback with custom SolFlash17 handler. Uses f17/f17b light objects. Lamp 117.
- `games/congo.json#/coils/12._vbscript_callback`: SetModLampm 118, 138,
- `games/congo.json#/coils/12._inferred_type`: flasher
- `games/congo.json#/coils/12._note`: SolModCallback. Drives lamp IDs 118 and 138.
- `games/congo.json#/coils/13._vbscript_callback`: SetModLampm 119, 129,
- `games/congo.json#/coils/13._inferred_type`: flasher
- `games/congo.json#/coils/13._note`: SolModCallback. Drives lamp IDs 119 and 129.
- `games/congo.json#/coils/14._vbscript_callback`: SetModLampm 120, 130,
- `games/congo.json#/coils/14._inferred_type`: flasher
- `games/congo.json#/coils/14._note`: SolModCallback. Drives lamp IDs 120 and 130.
- `games/congo.json#/coils/15._vbscript_callback`: SetModLamp 121,
- `games/congo.json#/coils/15._inferred_type`: flasher
- `games/congo.json#/coils/15._note`: SolModCallback. Drives lamp ID 121.
- `games/congo.json#/coils/16._vbscript_callback`: MapKick
- `games/congo.json#/coils/16._inferred_type`: ball_management
- `games/congo.json#/coils/16._note`: Ejects from bsMap (cvpmSaucer at sw38).
- `games/congo.json#/coils/17._vbscript_callback`: LeftGateOn
- `games/congo.json#/coils/17._inferred_type`: gate
- `games/congo.json#/coils/17._note`: Opens/closes gate2 object.
- `games/congo.json#/coils/18._vbscript_callback`: RightGateOn
- `games/congo.json#/coils/18._inferred_type`: gate
- `games/congo.json#/coils/18._note`: Opens/closes gate4 object.
- `games/congo.json#/coils/19._vbscript_callback`: SetModLampm 125, 135,
- `games/congo.json#/coils/19._inferred_type`: flasher
- `games/congo.json#/coils/19._note`: SolModCallback. Drives lamp IDs 125 and 135.
- `games/congo.json#/coils/20._vbscript_callback`: SetModLampm 126, 136,
- `games/congo.json#/coils/20._inferred_type`: flasher
- `games/congo.json#/coils/20._note`: SolModCallback. Drives lamp IDs 126 and 136.
- `games/congo.json#/coils/21._vbscript_callback`: SetModLampM 127, 137,
- `games/congo.json#/coils/21._inferred_type`: flasher
- `games/congo.json#/coils/21._note`: SolModCallback. Drives lamp IDs 127 and 137.
- `games/congo.json#/coils/22._vbscript_callback`: Sol28
- `games/congo.json#/coils/22._inferred_type`: flasher
- `games/congo.json#/coils/22._note`: SolModCallback with custom Sol28 handler. Drives f28/F28B light objects. Uses lamp 128 GI scale. Comment: 'old style'.
- `games/congo.json#/coils/23._vbscript_callback`: SolLeftpost
- `games/congo.json#/coils/23._inferred_type`: mechanism
- `games/congo.json#/coils/23._note`: Drops/raises LeftPost and LeftPost_invis. Plays buzz sound when energized.
- `games/congo.json#/coils/24._vbscript_callback`: MysteryKick
- `games/congo.json#/coils/24._inferred_type`: ball_management
- `games/congo.json#/coils/24._note`: Ejects from bsMystery (cvpmSaucer at sw37).
- `games/congo.json#/_source/confidence_notes`: High confidence on switches/coils from Controller.Switch() calls, PulseSw calls, and SolCallback/SolModCallback assignments. No Const sw* declarations in table script — all switches referenced by raw number. Lamp IDs from NFadeL/NFadeLm/NFadeLwF calls in UpdateLamps. Flashers (coils 17-21, 25-28) use SolModCallback with SetModLamp/SetModLampm routines or custom Sol28 callback. Trough is a 4-ball cvpmTrough with switches 32-35 and eject via BallRelease kicker (solenoid 9, fires PulseSw 31). Volcano is a separate cvpmTrough (switches 41-43, sol 6). Two-way popper (bsAmyVuk) is cvpmSaucer on switch 53 with two kick directions (sol 3 up, sol 4 down). Mystery saucer (sw37, sol 34) and Map saucer (sw38, sol 22). Upper left flipper present (sULFlipper=34), no upper right flipper. Grey Gorilla mechanism driven by solenoids 15/16. Header comment says Williams 1988 but game is actually Williams 1995.

## Unresolved questions

- Is the I/O enumeration complete for every supported physical/controller variant?
- Which inferred VPX behaviors reflect real hardware, and which are table-script conveniences?
- Are all mechanism home states, sensors, motion constraints, and ball interactions documented?

## Sources

- `legacy.game.congo`: `games/congo.json` at the pinned migration revision.
