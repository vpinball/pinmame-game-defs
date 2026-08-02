# Black Rose

Coverage: **partial - source-derived recreation knowledge requiring validation**

## Overview

Legacy evidence identifies this candidate as Bally (1992). The information below is preserved for recreation work but is not automatically treated as validated physical-machine fact.

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
- `games/br.json#/switches/1._note`: vpmNudge.TiltSwitch = 14
- `games/br.json#/switches/2._note`: bsTrough.EntrySw = 15
- `games/br.json#/switches/3._note`: bsTrough.initSwitches Array(16,17,18)
- `games/br.json#/switches/7._note`: Controller.Switch(22) = 1 in Table1_Init
- `games/br.json#/switches/8._note`: Controller.Switch(25) set in ShooterLane_Hit/UnHit
- `games/br.json#/switches/9._note`: Controller.Switch(26) set in Sw26_Hit/UnHit
- `games/br.json#/switches/10._note`: Controller.Switch(27) set in Sw27_Hit/UnHit
- `games/br.json#/switches/11._note`: PulseSw(28) in LeftSlingShot_Slingshot
- `games/br.json#/switches/12._note`: PulseSw(31) in Sw31_Hit
- `games/br.json#/switches/13._note`: PulseSw(32) in Sw32_Hit
- `games/br.json#/switches/14._note`: PulseSw(33) in Sw33_Hit
- `games/br.json#/switches/15._note`: Controller.Switch(34) set via PlungerKey in KeyDown/KeyUp
- `games/br.json#/switches/16._note`: Controller.Switch(35) = 1 in sw66_Sub_Hit (subway loads cannon); cleared by FireCannon
- `games/br.json#/switches/17._note`: Controller.Switch(36) set in Sw36_Hit/UnHit
- `games/br.json#/switches/18._note`: Controller.Switch(37) set in Sw37_Hit/UnHit
- `games/br.json#/switches/19._note`: PulseSw(38) in RightSlingShot_Slingshot
- `games/br.json#/switches/20._note`: PulseSw(41) in Sw41_Hit
- `games/br.json#/switches/21._note`: PulseSw(42) in Sw42_Hit
- `games/br.json#/switches/22._note`: PulseSw(43) in Sw43_Hit
- `games/br.json#/switches/23._note`: PulseSw(44) in GateSw44_Hit
- `games/br.json#/switches/24._note`: Controller.Switch(45) set in Sw45_Hit/UnHit
- `games/br.json#/switches/25._note`: PulseSw(46) in Bumper1_Hit
- `games/br.json#/switches/26._note`: PulseSw(47) in Bumper2_Hit
- `games/br.json#/switches/27._note`: PulseSw(48) in BumperSw48_Hit
- `games/br.json#/switches/28._note`: PulseSw(51) in Sw51_Hit
- `games/br.json#/switches/29._note`: PulseSw(52) in Sw52_Hit
- `games/br.json#/switches/30._note`: PulseSw(53) in Sw53_Hit
- `games/br.json#/switches/31._note`: Controller.Switch(54) managed by RampDown/RampUp solenoid callbacks; indicates ship ramp (Davey Jones) is in down position
- `games/br.json#/switches/32._note`: Controller.Switch(55) = 1 in KickerSW55_Hit; cleared by RampSwordKicker
- `games/br.json#/switches/33._note`: Controller.Switch(56) set in Sw56_Hit/UnHit
- `games/br.json#/switches/34._note`: Controller.Switch(57) set in Sw57_Hit/UnHit
- `games/br.json#/switches/35._note`: Controller.Switch(58) set in Sw58_Hit/UnHit
- `games/br.json#/switches/36._note`: PulseSwitch 61 in sw61_Sub_Hit
- `games/br.json#/switches/37._note`: Controller.Switch(62) set in Sw62_Hit/UnHit
- `games/br.json#/switches/38._note`: Controller.Switch(63) = 1 in KickerSw63_Hit; cleared by PiratesCoveKick
- `games/br.json#/switches/39._note`: Controller.Switch(64) = 1 in KickerSw64_Hit; cleared by PiratesCoveKick
- `games/br.json#/switches/40._note`: PulseSw(65) in Sw65_Hit
- `games/br.json#/switches/41._note`: PulseSwitch 66 in sw66_Sub_Hit; also sets Controller.Switch(35) = 1
- `games/br.json#/switches/42._note`: PulseSw(71) in GateSw71_Hit
- `games/br.json#/switches/43._note`: PulseSw(72) in GateSw72_Hit
- `games/br.json#/switches/44._note`: PulseSw(76) in GateSw76_Hit
- `games/br.json#/coils/0._vbscript_callback`: RampSwordKicker
- `games/br.json#/coils/0._inferred_type`: kicker
- `games/br.json#/coils/0._note`: Destroys ball at KickerSw55, creates at KickerSW55Upper, kicks 180/5
- `games/br.json#/coils/1._vbscript_callback`: bsTroughSolIn
- `games/br.json#/coils/1._inferred_type`: ball_management
- `games/br.json#/coils/2._vbscript_callback`: CannonMotor
- `games/br.json#/coils/2._inferred_type`: mechanism
- `games/br.json#/coils/2._note`: Enables DiscTimer to rotate cannon; plays Motor_Cannon loop sound
- `games/br.json#/coils/3._vbscript_callback`: bsTroughSolOut
- `games/br.json#/coils/3._inferred_type`: ball_management
- `games/br.json#/coils/3._note`: bsTrough.InitExit BallRelease, 55, 8
- `games/br.json#/coils/4._note`: Empty SolCallback in script
- `games/br.json#/coils/5._note`: Empty SolCallback in script
- `games/br.json#/coils/6._vbscript_callback`: SolKnocker
- `games/br.json#/coils/6._inferred_type`: knocker
- `games/br.json#/coils/7._vbscript_callback`: FireCannon
- `games/br.json#/coils/7._inferred_type`: mechanism
- `games/br.json#/coils/7._note`: Creates ball at CannonKicker, kicks at disc angle; clears sw35
- `games/br.json#/coils/8._vbscript_callback`: PiratesCoveKick
- `games/br.json#/coils/8._inferred_type`: kicker
- `games/br.json#/coils/8._note`: Kicks from KickerSw64 first, then KickerSw63; clears sw63/sw64
- `games/br.json#/coils/9._vbscript_callback`: RampUp
- `games/br.json#/coils/9._inferred_type`: mechanism
- `games/br.json#/coils/9._note`: Clears Controller.Switch(54); raises DaveyRamp via timer
- `games/br.json#/coils/10._vbscript_callback`: RampDown
- `games/br.json#/coils/10._inferred_type`: mechanism
- `games/br.json#/coils/10._note`: Sets Controller.Switch(54) = 1; lowers DaveyRamp via timer
- `games/br.json#/coils/11._note`: Empty SolCallback in script
- `games/br.json#/coils/12._note`: Empty SolCallback in script
- `games/br.json#/coils/13._note`: Empty SolCallback in script
- `games/br.json#/coils/14._note`: Empty SolCallback in script
- `games/br.json#/coils/15._note`: Empty SolCallback in script
- `games/br.json#/coils/16._vbscript_callback`: Sol17
- `games/br.json#/coils/16._inferred_type`: flasher
- `games/br.json#/coils/16._note`: Backglass: Top 'Black'; SetLamp 117
- `games/br.json#/coils/17._vbscript_callback`: Sol18
- `games/br.json#/coils/17._inferred_type`: flasher
- `games/br.json#/coils/17._note`: Backglass: Lady Pirate Belly; SetLamp 118
- `games/br.json#/coils/18._vbscript_callback`: Sol19
- `games/br.json#/coils/18._inferred_type`: flasher
- `games/br.json#/coils/18._note`: Backglass: Man Pirate Right; SetLamp 119
- `games/br.json#/coils/19._vbscript_callback`: Sol20
- `games/br.json#/coils/19._inferred_type`: flasher
- `games/br.json#/coils/19._note`: Backglass: Right Top; SetLamp 120
- `games/br.json#/coils/20._vbscript_callback`: Sol21
- `games/br.json#/coils/20._inferred_type`: flasher
- `games/br.json#/coils/20._note`: Backglass: Bottom 'Rose'; SetLamp 121
- `games/br.json#/coils/21._vbscript_callback`: Sol22
- `games/br.json#/coils/21._inferred_type`: flasher
- `games/br.json#/coils/21._note`: Backglass: Bottom 'Black'; SetLamp 122
- `games/br.json#/coils/22._vbscript_callback`: Sol23
- `games/br.json#/coils/22._inferred_type`: flasher
- `games/br.json#/coils/22._note`: Backglass: Skull; SetLamp 123
- `games/br.json#/coils/23._vbscript_callback`: Sol24
- `games/br.json#/coils/23._inferred_type`: flasher
- `games/br.json#/coils/23._note`: Backglass: Bottom of Skull; SetLamp 124
- `games/br.json#/coils/24._vbscript_callback`: SetLamp 125,
- `games/br.json#/coils/24._inferred_type`: flasher
- `games/br.json#/coils/24._note`: SolModCallback uses SetLamp 125 directly (no Sol25 sub)
- `games/br.json#/coils/25._vbscript_callback`: SetLamp 126,
- `games/br.json#/coils/25._inferred_type`: flasher
- `games/br.json#/coils/25._note`: Dual cannon flashers; SolModCallback uses SetLamp 126 directly (no Sol26 sub)
- `games/br.json#/coils/26._vbscript_callback`: Sol27
- `games/br.json#/coils/26._inferred_type`: flasher
- `games/br.json#/coils/26._note`: Backglass: Canon Flame; SetLamp 127
- `games/br.json#/coils/27._vbscript_callback`: Sol28
- `games/br.json#/coils/27._inferred_type`: flasher
- `games/br.json#/coils/27._note`: Backglass: Middle Pirate; SetLamp 128
- `games/br.json#/lamps/38._note`: Lampz.Callback(57) commented out in VBS
- `games/br.json#/lamps/45._note`: Lampz.Callback(66) commented out in VBS
- `games/br.json#/lamps/60._note`: Also controls secondary insert (l86a / Pot)
- `games/br.json#/_source/confidence_notes`: High confidence on switches and coils — extracted from VPW v1.4 VBScript. No Const sw*/s* declarations in script; switches identified from _Hit/_UnHit subs, Controller.Switch() calls, PulseSw() calls, and bsTrough.initSwitches. Lamps from Lampz.MassAssign; lamp descriptions inferred from playfield layout and rulesheet — lower confidence than switches/coils. Flasher coils 17-24,27-28 use SolModCallback with Sol## subs; flashers 25-26 use SolModCallback with SetLamp directly. Flipper solenoid IDs use framework constants (sLRFlipper, sLLFlipper, sURFlipper) from core.vbs — not extracted as game-level coils. Solenoids 5-6, 12-16 have empty callbacks in script. Switches 13 (Start), 21 (Slam Tilt), 22 (Coin Door) are framework-handled. Switch 23 (Ticket Opto) not referenced in this VPW script. IPDB URL in script header points to id=313.

## Unresolved questions

- Is the I/O enumeration complete for every supported physical/controller variant?
- Which inferred VPX behaviors reflect real hardware, and which are table-script conveniences?
- Are all mechanism home states, sensors, motion constraints, and ball interactions documented?

## Sources

- `legacy.game.br`: `games/br.json` at the pinned migration revision.
