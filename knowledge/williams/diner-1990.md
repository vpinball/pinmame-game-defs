# Diner

Coverage: **partial - source-derived recreation knowledge requiring validation**

## Overview

Legacy evidence identifies this candidate as Williams (1990). The information below is preserved for recreation work but is not automatically treated as validated physical-machine fact.

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

- `games/diner.json#/switches/0._vbscript_name`: swOuthole
- `games/diner.json#/switches/1._vbscript_name`: swUpDownRamp
- `games/diner.json#/switches/1._note`: Also used as bsTrough.EntrySw (trough entry switch)
- `games/diner.json#/switches/2._vbscript_name`: swTrough1
- `games/diner.json#/switches/3._vbscript_name`: swTrough2
- `games/diner.json#/switches/4._vbscript_name`: swTrough3
- `games/diner.json#/switches/5._vbscript_name`: swShooterLane
- `games/diner.json#/switches/6._vbscript_name`: swSubPlfdShooter1
- `games/diner.json#/switches/7._vbscript_name`: swSubPlfdShooter2
- `games/diner.json#/switches/8._vbscript_name`: swCup
- `games/diner.json#/switches/9._vbscript_name`: swGrillBonus
- `games/diner.json#/switches/10._vbscript_name`: swE
- `games/diner.json#/switches/11._vbscript_name`: swA
- `games/diner.json#/switches/12._vbscript_name`: swT
- `games/diner.json#/switches/13._vbscript_name`: swHotdog
- `games/diner.json#/switches/14._vbscript_name`: swBurger
- `games/diner.json#/switches/15._vbscript_name`: swChili
- `games/diner.json#/switches/16._vbscript_name`: swRightRampEntry
- `games/diner.json#/switches/17._vbscript_name`: swRightRampExit
- `games/diner.json#/switches/18._vbscript_name`: swCupEntry
- `games/diner.json#/switches/19._vbscript_name`: swRootBeer
- `games/diner.json#/switches/20._vbscript_name`: swFries
- `games/diner.json#/switches/21._vbscript_name`: swIcedTea
- `games/diner.json#/switches/22._vbscript_name`: swLeftRampExit
- `games/diner.json#/switches/23._vbscript_name`: swLeftOutlane
- `games/diner.json#/switches/24._vbscript_name`: swLeftReturnLane
- `games/diner.json#/switches/25._vbscript_name`: swRightReturnLane
- `games/diner.json#/switches/26._vbscript_name`: swRightOutlane
- `games/diner.json#/switches/27._vbscript_name`: swUpperLeftEject
- `games/diner.json#/switches/28._vbscript_name`: swLowerLeftEject
- `games/diner.json#/switches/29._vbscript_name`: swLeftJetBumper
- `games/diner.json#/switches/30._vbscript_name`: swRightJetBumper
- `games/diner.json#/switches/31._vbscript_name`: swLowerJetBumper
- `games/diner.json#/switches/32._vbscript_name`: swBRKicker
- `games/diner.json#/switches/32._vbscript_alias`: swRSling
- `games/diner.json#/switches/33._vbscript_name`: swBLKicker
- `games/diner.json#/switches/33._vbscript_alias`: swLSling
- `games/diner.json#/switches/34._vbscript_name`: swSpinner
- `games/diner.json#/switches/35._vbscript_name`: swFlipR
- `games/diner.json#/switches/36._vbscript_name`: swFlipL
- `games/diner.json#/switches/37._vbscript_name`: swClockWheel
- `games/diner.json#/coils/0._vbscript_name`: sOuthole
- `games/diner.json#/coils/0._vbscript_callback`: bsTrough.SolIn
- `games/diner.json#/coils/0._inferred_type`: ball_management
- `games/diner.json#/coils/1._vbscript_name`: sRampDown
- `games/diner.json#/coils/1._vbscript_callback`: SolRampDown
- `games/diner.json#/coils/1._inferred_type`: mechanism
- `games/diner.json#/coils/2._vbscript_name`: sC3BDTReset
- `games/diner.json#/coils/2._vbscript_callback`: SolDTBankMiddle
- `games/diner.json#/coils/2._inferred_type`: drop_target_reset
- `games/diner.json#/coils/3._vbscript_name`: sRampUp
- `games/diner.json#/coils/3._vbscript_callback`: SolRampUp
- `games/diner.json#/coils/3._inferred_type`: mechanism
- `games/diner.json#/coils/4._vbscript_name`: sUpperLeftEject
- `games/diner.json#/coils/4._vbscript_callback`: SolUpperEject
- `games/diner.json#/coils/4._inferred_type`: kicker
- `games/diner.json#/coils/5._vbscript_name`: sSubPlfdShooter
- `games/diner.json#/coils/5._vbscript_callback`: SolSubPlfdShooter
- `games/diner.json#/coils/5._inferred_type`: kicker
- `games/diner.json#/coils/6._vbscript_name`: sKnocker
- `games/diner.json#/coils/6._vbscript_callback`: SolKnocker
- `games/diner.json#/coils/6._inferred_type`: knocker
- `games/diner.json#/coils/7._vbscript_name`: sLowerLeftEject
- `games/diner.json#/coils/7._vbscript_callback`: SolLowKicker
- `games/diner.json#/coils/7._inferred_type`: kicker
- `games/diner.json#/coils/8._vbscript_name`: sRightRampFlasher
- `games/diner.json#/coils/8._vbscript_callback`: SolFlash9
- `games/diner.json#/coils/8._inferred_type`: flasher
- `games/diner.json#/coils/8._note`: BG Moon
- `games/diner.json#/coils/9._vbscript_name`: sBackBoxRelay
- `games/diner.json#/coils/9._vbscript_callback`: SolGIRelay
- `games/diner.json#/coils/9._inferred_type`: gi_relay
- `games/diner.json#/coils/10._vbscript_name`: sLeftRampFlasher
- `games/diner.json#/coils/10._vbscript_callback`: SolFlash11
- `games/diner.json#/coils/10._inferred_type`: flasher
- `games/diner.json#/coils/10._note`: BG Diner
- `games/diner.json#/coils/11._vbscript_name`: sACselectrelay
- `games/diner.json#/coils/11._vbscript_callback`: SolACSelect
- `games/diner.json#/coils/11._inferred_type`: relay
- `games/diner.json#/coils/12._vbscript_name`: sL3BDTReset
- `games/diner.json#/coils/12._vbscript_callback`: SolDTBankLeft
- `games/diner.json#/coils/12._inferred_type`: drop_target_reset
- `games/diner.json#/coils/13._vbscript_callback`: Sol14Diverter
- `games/diner.json#/coils/13._inferred_type`: diverter
- `games/diner.json#/coils/13._note`: No named constant — referenced by number in SolCallback
- `games/diner.json#/coils/14._vbscript_name`: sClockWheel
- `games/diner.json#/coils/14._inferred_type`: mechanism
- `games/diner.json#/coils/15._vbscript_name`: sLeftJetBumper
- `games/diner.json#/coils/15._inferred_type`: bumper
- `games/diner.json#/coils/15._note`: SolCallback commented out in script
- `games/diner.json#/coils/16._vbscript_name`: sLSling
- `games/diner.json#/coils/16._inferred_type`: slingshot
- `games/diner.json#/coils/17._vbscript_name`: sRightJetBumper
- `games/diner.json#/coils/17._inferred_type`: bumper
- `games/diner.json#/coils/17._note`: SolCallback commented out in script
- `games/diner.json#/coils/18._vbscript_name`: sRSling
- `games/diner.json#/coils/18._inferred_type`: slingshot
- `games/diner.json#/coils/19._vbscript_name`: sLowerJetBumper
- `games/diner.json#/coils/19._inferred_type`: bumper
- `games/diner.json#/coils/19._note`: SolCallback commented out in script
- `games/diner.json#/coils/20._vbscript_name`: sShooterLaneFeeder
- `games/diner.json#/coils/20._vbscript_callback`: bsTrough.SolOut
- `games/diner.json#/coils/20._inferred_type`: ball_management
- `games/diner.json#/coils/21._vbscript_callback`: TiltSol
- `games/diner.json#/coils/21._inferred_type`: tilt
- `games/diner.json#/coils/21._note`: No named constant — referenced by number in SolCallback
- `games/diner.json#/coils/22._vbscript_callback`: SolHajiF
- `games/diner.json#/coils/22._inferred_type`: flasher
- `games/diner.json#/coils/22._note`: BG Haji character flasher. No named constant.
- `games/diner.json#/coils/23._vbscript_callback`: SolBabsF
- `games/diner.json#/coils/23._inferred_type`: flasher
- `games/diner.json#/coils/23._note`: BG Babs character flasher. No named constant.
- `games/diner.json#/coils/24._vbscript_callback`: SolBorisF
- `games/diner.json#/coils/24._inferred_type`: flasher
- `games/diner.json#/coils/24._note`: BG Boris character flasher. No named constant.
- `games/diner.json#/coils/25._vbscript_callback`: SolPepeF
- `games/diner.json#/coils/25._inferred_type`: flasher
- `games/diner.json#/coils/25._note`: BG Pepe character flasher. No named constant.
- `games/diner.json#/coils/26._vbscript_callback`: SolBuckF
- `games/diner.json#/coils/26._inferred_type`: flasher
- `games/diner.json#/coils/26._note`: BG Buck character flasher. No named constant.
- `games/diner.json#/coils/27._vbscript_callback`: SolCupF
- `games/diner.json#/coils/27._inferred_type`: flasher
- `games/diner.json#/coils/27._note`: No named constant.
- `games/diner.json#/coils/28._vbscript_callback`: Sol31
- `games/diner.json#/coils/28._inferred_type`: flasher
- `games/diner.json#/coils/28._note`: BG clock (2). No named constant.
- `games/diner.json#/coils/29._vbscript_name`: sDineTF
- `games/diner.json#/coils/29._vbscript_callback`: Sol32
- `games/diner.json#/coils/29._inferred_type`: flasher
- `games/diner.json#/coils/29._note`: BG Dine Time (2)
- `games/diner.json#/coils/30._vbscript_name`: sLRFlipper
- `games/diner.json#/coils/30._vbscript_callback`: SolRFlipper
- `games/diner.json#/coils/30._inferred_type`: flipper
- `games/diner.json#/coils/30._note`: Framework-defined constant (core.vbs: sLRFlipper=46)
- `games/diner.json#/coils/31._vbscript_name`: sLLFlipper
- `games/diner.json#/coils/31._vbscript_callback`: SolLFlipper
- `games/diner.json#/coils/31._inferred_type`: flipper
- `games/diner.json#/coils/31._note`: Framework-defined constant (core.vbs: sLLFlipper=48)
- `games/diner.json#/lamps/0._light_type`: 1
- `games/diner.json#/lamps/1._light_type`: 1
- `games/diner.json#/lamps/2._light_type`: 1
- `games/diner.json#/lamps/3._light_type`: 1
- `games/diner.json#/lamps/4._light_type`: 1
- `games/diner.json#/lamps/5._light_type`: 0
- `games/diner.json#/lamps/6._light_type`: 0
- `games/diner.json#/lamps/7._light_type`: 0
- `games/diner.json#/lamps/8._light_type`: 0
- `games/diner.json#/lamps/9._light_type`: 0
- `games/diner.json#/lamps/10._light_type`: 0
- `games/diner.json#/lamps/11._light_type`: 0
- `games/diner.json#/lamps/12._light_type`: 0
- `games/diner.json#/lamps/13._light_type`: 0
- `games/diner.json#/lamps/14._light_type`: 0
- `games/diner.json#/lamps/15._light_type`: 0
- `games/diner.json#/lamps/16._light_type`: 0
- `games/diner.json#/lamps/17._light_type`: 0
- `games/diner.json#/lamps/18._light_type`: 0
- `games/diner.json#/lamps/19._light_type`: 0
- `games/diner.json#/lamps/20._light_type`: 0
- `games/diner.json#/lamps/21._light_type`: 2
- `games/diner.json#/lamps/21._note`: EAT multi-light with circleE insert
- `games/diner.json#/lamps/22._light_type`: 2
- `games/diner.json#/lamps/22._note`: EAT multi-light with circleA insert
- `games/diner.json#/lamps/23._light_type`: 2
- `games/diner.json#/lamps/23._note`: EAT multi-light with circleT insert
- `games/diner.json#/lamps/24._light_type`: 1
- `games/diner.json#/lamps/25._light_type`: 1
- `games/diner.json#/lamps/26._light_type`: 1
- `games/diner.json#/lamps/27._light_type`: 1
- `games/diner.json#/lamps/28._light_type`: 1
- `games/diner.json#/lamps/29._light_type`: 0
- `games/diner.json#/lamps/30._light_type`: 0
- `games/diner.json#/lamps/31._light_type`: 0
- `games/diner.json#/lamps/32._light_type`: 3
- `games/diner.json#/lamps/32._note`: Cutout flasher — backbox character
- `games/diner.json#/lamps/33._light_type`: 3
- `games/diner.json#/lamps/33._note`: Cutout flasher — backbox character
- `games/diner.json#/lamps/34._light_type`: 3
- `games/diner.json#/lamps/34._note`: Cutout flasher — backbox character
- `games/diner.json#/lamps/35._light_type`: 3
- `games/diner.json#/lamps/35._note`: Cutout flasher — backbox character
- `games/diner.json#/lamps/36._light_type`: 3
- `games/diner.json#/lamps/36._note`: Cutout flasher — backbox character
- `games/diner.json#/lamps/37._light_type`: 0
- `games/diner.json#/lamps/38._light_type`: 0
- `games/diner.json#/lamps/39._light_type`: 0
- `games/diner.json#/lamps/40._light_type`: 0
- `games/diner.json#/lamps/41._light_type`: 0
- `games/diner.json#/lamps/42._light_type`: 0
- `games/diner.json#/lamps/43._light_type`: 0
- `games/diner.json#/lamps/44._light_type`: 0
- `games/diner.json#/lamps/45._light_type`: 0
- `games/diner.json#/lamps/46._light_type`: 0
- `games/diner.json#/lamps/47._light_type`: 0
- `games/diner.json#/lamps/48._light_type`: 1
- `games/diner.json#/lamps/48._note`: Clock lights 49-60 only active in VR mode; type 4 (not connected) otherwise
- `games/diner.json#/lamps/49._light_type`: 1
- `games/diner.json#/lamps/49._note`: VR mode only
- `games/diner.json#/lamps/50._light_type`: 1
- `games/diner.json#/lamps/50._note`: VR mode only
- `games/diner.json#/lamps/51._light_type`: 1
- `games/diner.json#/lamps/51._note`: VR mode only
- `games/diner.json#/lamps/52._light_type`: 1
- `games/diner.json#/lamps/52._note`: VR mode only
- `games/diner.json#/lamps/53._light_type`: 1
- `games/diner.json#/lamps/53._note`: VR mode only
- `games/diner.json#/lamps/54._light_type`: 1
- `games/diner.json#/lamps/54._note`: VR mode only
- `games/diner.json#/lamps/55._light_type`: 1
- `games/diner.json#/lamps/55._note`: VR mode only
- `games/diner.json#/lamps/56._light_type`: 1
- `games/diner.json#/lamps/56._note`: VR mode only
- `games/diner.json#/lamps/57._light_type`: 1
- `games/diner.json#/lamps/57._note`: VR mode only
- `games/diner.json#/lamps/58._light_type`: 1
- `games/diner.json#/lamps/58._note`: VR mode only
- `games/diner.json#/lamps/59._light_type`: 1
- `games/diner.json#/lamps/59._note`: VR mode only
- `games/diner.json#/lamps/60._light_type`: 0
- `games/diner.json#/lamps/61._light_type`: 0
- `games/diner.json#/lamps/62._light_type`: 0
- `games/diner.json#/lamps/63._light_type`: 0
- `games/diner.json#/lamps/64._light_type`: 4
- `games/diner.json#/lamps/64._note`: Defined but type 4 (not connected)
- `games/diner.json#/_source/confidence_notes`: High confidence on switches/coils/lamps. Uses S11.VBS (System 11, not WPC). swBRKicker(54)/swBLKicker(55) overlap with swRSling(54)/swLSling(55) — same physical switches, dual names. sLRFlipper, sLLFlipper, swTroughEject are framework-defined (core.vbs/S11.VBS), not in table script. Lamps 49-60 (clock lights) only active in VR mode; type 4 (not connected) in non-VR. Commented-out SolCallbacks for jet bumpers included as coils without callbacks.

## Unresolved questions

- Is the I/O enumeration complete for every supported physical/controller variant?
- Which inferred VPX behaviors reflect real hardware, and which are table-script conveniences?
- Are all mechanism home states, sensors, motion constraints, and ball interactions documented?

## Sources

- `legacy.game.diner`: `games/diner.json` at the pinned migration revision.
