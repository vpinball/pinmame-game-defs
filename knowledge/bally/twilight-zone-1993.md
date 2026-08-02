# Twilight Zone

Coverage: **partial - source-derived recreation knowledge requiring validation**

## Overview

Legacy evidence identifies this candidate as Bally (1993). The information below is preserved for recreation work but is not automatically treated as validated physical-machine fact.

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
- `games/tz.json#/switches/0._inferred_type`: rollover
- `games/tz.json#/switches/1._inferred_type`: rollover
- `games/tz.json#/switches/3._note`: vpmNudge.TiltSwitch = 14
- `games/tz.json#/switches/4._note`: Opto; also used for powerball detection via sw26
- `games/tz.json#/switches/9._note`: Controller.Switch(22) = 1 on init
- `games/tz.json#/switches/10._note`: Mapped to KeyFront
- `games/tz.json#/switches/12._note`: Opto; 1 if regular ball in sw15, 0 if powerball
- `games/tz.json#/switches/13._inferred_type`: shooter_lane
- `games/tz.json#/switches/14._inferred_type`: kicker
- `games/tz.json#/switches/15._inferred_type`: bumper
- `games/tz.json#/switches/16._inferred_type`: bumper
- `games/tz.json#/switches/17._inferred_type`: bumper
- `games/tz.json#/switches/18._note`: LeftSlingShot fires PulseSw 34 (cross-wired naming in script)
- `games/tz.json#/switches/19._note`: RightSlingShot fires PulseSw 35 (cross-wired naming in script)
- `games/tz.json#/switches/20._inferred_type`: rollover
- `games/tz.json#/switches/21._inferred_type`: rollover
- `games/tz.json#/switches/22._inferred_type`: rollover
- `games/tz.json#/switches/23._note`: Also triggered by RightSlingShot_Slingshot
- `games/tz.json#/switches/24._note`: Submarine switch; also triggered by LeftSlingShot_Slingshot
- `games/tz.json#/switches/25._inferred_type`: submarine_switch
- `games/tz.json#/switches/27._note`: sw45a also triggers this switch
- `games/tz.json#/switches/28._note`: sw46a also triggers this switch
- `games/tz.json#/switches/29._inferred_type`: standup_target
- `games/tz.json#/switches/30._inferred_type`: standup_target
- `games/tz.json#/switches/31._inferred_type`: hole
- `games/tz.json#/switches/32._inferred_type`: rollover
- `games/tz.json#/switches/33._inferred_type`: ramp_switch
- `games/tz.json#/switches/34._inferred_type`: ramp_switch
- `games/tz.json#/switches/35._note`: Pulsed by SolGumRelease timer; not a physical VPX object
- `games/tz.json#/switches/36._inferred_type`: rollover
- `games/tz.json#/switches/37._note`: Submarine switch; only triggers for non-powerball
- `games/tz.json#/switches/38._inferred_type`: kicker
- `games/tz.json#/switches/39._inferred_type`: rollover
- `games/tz.json#/switches/40._inferred_type`: rollover
- `games/tz.json#/switches/41._inferred_type`: rollover
- `games/tz.json#/switches/42._inferred_type`: standup_target
- `games/tz.json#/switches/43._note`: sw65a fires STHit 165 (virtual duplicate)
- `games/tz.json#/switches/43._inferred_type`: standup_target
- `games/tz.json#/switches/44._inferred_type`: standup_target
- `games/tz.json#/switches/45._inferred_type`: standup_target
- `games/tz.json#/switches/46._inferred_type`: standup_target
- `games/tz.json#/switches/47._inferred_type`: kicker
- `games/tz.json#/switches/48._inferred_type`: ramp_switch
- `games/tz.json#/switches/49._inferred_type`: kicker
- `games/tz.json#/switches/52._inferred_type`: standup_target
- `games/tz.json#/switches/53._inferred_type`: standup_target
- `games/tz.json#/switches/54._inferred_type`: opto
- `games/tz.json#/switches/55._inferred_type`: opto
- `games/tz.json#/switches/55._note`: Only enabled when Extra Magnet mod is on
- `games/tz.json#/switches/56._inferred_type`: opto
- `games/tz.json#/switches/57._inferred_type`: lock
- `games/tz.json#/switches/58._inferred_type`: lock
- `games/tz.json#/switches/59._note`: Only in prototypes, supported by ROM 9.4
- `games/tz.json#/switches/59._inferred_type`: opto
- `games/tz.json#/switches/60._inferred_type`: opto
- `games/tz.json#/switches/61._inferred_type`: lock
- `games/tz.json#/coils/0._vbscript_callback`: SlotMachineKickout
- `games/tz.json#/coils/0._inferred_type`: kicker
- `games/tz.json#/coils/1._vbscript_callback`: SolRocket
- `games/tz.json#/coils/1._inferred_type`: kicker
- `games/tz.json#/coils/2._vbscript_callback`: SolAutoKicker
- `games/tz.json#/coils/2._inferred_type`: ball_management
- `games/tz.json#/coils/3._vbscript_callback`: SolGumballPopper
- `games/tz.json#/coils/3._inferred_type`: kicker
- `games/tz.json#/coils/4._vbscript_callback`: SolRightRampDiverter
- `games/tz.json#/coils/4._inferred_type`: diverter
- `games/tz.json#/coils/5._vbscript_callback`: SolGumballDiverter
- `games/tz.json#/coils/5._inferred_type`: diverter
- `games/tz.json#/coils/6._vbscript_callback`: SolKnocker
- `games/tz.json#/coils/6._inferred_type`: sound
- `games/tz.json#/coils/7._vbscript_callback`: SolOuthole
- `games/tz.json#/coils/7._inferred_type`: ball_management
- `games/tz.json#/coils/8._vbscript_callback`: SolBallRelease
- `games/tz.json#/coils/8._inferred_type`: ball_management
- `games/tz.json#/coils/9._inferred_type`: slingshot
- `games/tz.json#/coils/9._note`: Commented out in script; handled by VPX physics
- `games/tz.json#/coils/10._inferred_type`: slingshot
- `games/tz.json#/coils/10._note`: Commented out in script; handled by VPX physics
- `games/tz.json#/coils/11._inferred_type`: bumper
- `games/tz.json#/coils/11._note`: Commented out in script; handled by VPX physics
- `games/tz.json#/coils/12._inferred_type`: bumper
- `games/tz.json#/coils/12._note`: Commented out in script; handled by VPX physics
- `games/tz.json#/coils/13._inferred_type`: bumper
- `games/tz.json#/coils/13._note`: Commented out in script; handled by VPX physics
- `games/tz.json#/coils/14._vbscript_callback`: LockKickout
- `games/tz.json#/coils/14._inferred_type`: kicker
- `games/tz.json#/coils/15._vbscript_callback`: SolShootDiverter
- `games/tz.json#/coils/15._inferred_type`: diverter
- `games/tz.json#/coils/16._vbscript_callback`: UpdateF17
- `games/tz.json#/coils/16._inferred_type`: flasher
- `games/tz.json#/coils/16._note`: SolModCallback (PWM)
- `games/tz.json#/coils/17._vbscript_callback`: FlashPWM
- `games/tz.json#/coils/17._inferred_type`: flasher
- `games/tz.json#/coils/17._note`: SolModCallback (PWM)
- `games/tz.json#/coils/18._vbscript_callback`: FlashPWM
- `games/tz.json#/coils/18._inferred_type`: flasher
- `games/tz.json#/coils/18._note`: SolModCallback (PWM)
- `games/tz.json#/coils/19._vbscript_callback`: FlashPWM
- `games/tz.json#/coils/19._inferred_type`: flasher
- `games/tz.json#/coils/19._note`: SolModCallback (PWM)
- `games/tz.json#/coils/20._vbscript_callback`: SolLeftMagnet
- `games/tz.json#/coils/20._inferred_type`: magnet
- `games/tz.json#/coils/21._vbscript_callback`: SolUpperRightMagnet
- `games/tz.json#/coils/21._inferred_type`: magnet
- `games/tz.json#/coils/21._note`: Only present in mod-equipped tables
- `games/tz.json#/coils/22._vbscript_callback`: SolLowerRightMagnet
- `games/tz.json#/coils/22._inferred_type`: magnet
- `games/tz.json#/coils/23._vbscript_callback`: SolGumballMotor
- `games/tz.json#/coils/23._inferred_type`: mechanism
- `games/tz.json#/coils/24._vbscript_callback`: SolMiniMagnet mLeftMini,
- `games/tz.json#/coils/24._inferred_type`: magnet
- `games/tz.json#/coils/25._vbscript_callback`: SolMiniMagnet mRightMini,
- `games/tz.json#/coils/25._inferred_type`: magnet
- `games/tz.json#/coils/26._vbscript_callback`: SolLeftRampDiverter
- `games/tz.json#/coils/26._inferred_type`: diverter
- `games/tz.json#/coils/27._vbscript_callback`: FlashPWM
- `games/tz.json#/coils/27._inferred_type`: flasher
- `games/tz.json#/coils/27._note`: SolModCallback (PWM)
- `games/tz.json#/coils/28._vbscript_callback`: SolURFlipper
- `games/tz.json#/coils/28._inferred_type`: flipper
- `games/tz.json#/coils/28._note`: Framework constant sURFlipper=34 from core.vbs
- `games/tz.json#/coils/29._vbscript_callback`: SolULFlipper
- `games/tz.json#/coils/29._inferred_type`: flipper
- `games/tz.json#/coils/29._note`: Framework constant sULFlipper=36 from core.vbs
- `games/tz.json#/coils/30._vbscript_callback`: SolRFlipper
- `games/tz.json#/coils/30._inferred_type`: flipper
- `games/tz.json#/coils/30._note`: Framework constant sLRFlipper=46 from core.vbs
- `games/tz.json#/coils/31._vbscript_callback`: SolLFlipper
- `games/tz.json#/coils/31._inferred_type`: flipper
- `games/tz.json#/coils/31._note`: Framework constant sLLFlipper=48 from core.vbs
- `games/tz.json#/coils/32._vbscript_callback`: FlashPWM
- `games/tz.json#/coils/32._inferred_type`: flasher
- `games/tz.json#/coils/32._note`: SolModCallback (PWM); PinMAME coil 51 = flasher 37
- `games/tz.json#/coils/33._vbscript_callback`: FlashPWM
- `games/tz.json#/coils/33._inferred_type`: flasher
- `games/tz.json#/coils/33._note`: SolModCallback (PWM); PinMAME coil 52 = flasher 38
- `games/tz.json#/coils/34._vbscript_callback`: FlashPWM
- `games/tz.json#/coils/34._inferred_type`: flasher
- `games/tz.json#/coils/34._note`: SolModCallback (PWM); PinMAME coil 53 = flasher 39
- `games/tz.json#/coils/35._vbscript_callback`: FlashPWM
- `games/tz.json#/coils/35._inferred_type`: flasher
- `games/tz.json#/coils/35._note`: SolModCallback (PWM); PinMAME coil 54 = flasher 40
- `games/tz.json#/coils/36._vbscript_callback`: FlashPWM
- `games/tz.json#/coils/36._inferred_type`: flasher
- `games/tz.json#/coils/36._note`: SolModCallback (PWM); PinMAME coil 55 = flasher 41
- `games/tz.json#/coils/37._inferred_type`: mechanism
- `games/tz.json#/coils/37._note`: Commented out in script; PinMAME coil 56 = real coil 42
- `games/tz.json#/coils/38._inferred_type`: mechanism
- `games/tz.json#/coils/38._note`: Commented out in script; PinMAME coil 57 = real coil 43
- `games/tz.json#/coils/39._inferred_type`: mechanism
- `games/tz.json#/coils/39._note`: Commented out in script; PinMAME coil 58 = real coil 44
- `games/tz.json#/coils/40._inferred_type`: mechanism
- `games/tz.json#/coils/40._note`: PinMAME hack; commented out as unreliable with SolModCallbacks
- `games/tz.json#/lamps/51._note`: Listed as LM_Flashers_l74 in lightmap bake arrays
- `games/tz.json#/_source/confidence_notes`: High confidence on coils/SolCallbacks and switch handler mappings. No Const sw*/s* definitions in table script — this table uses raw switch numbers (Controller.Switch(N), vpmTimer.PulseSw N) and raw SolCallback(N) indices instead of named constants. Trough is custom-implemented (not bsTrough): sw15/sw16/sw17 are trough opto switches, sw25 is trough jam, sw18 is outhole, sw26 is powerball detect opto. Coils 10-14 (slings/bumpers) are commented out in script (handled by VPX physics). sLRFlipper(46)/sLLFlipper(48)/sURFlipper(34)/sULFlipper(36) are framework constants from core.vbs. Lamp numbers from vpmMapLights AllLamps (TimerInterval-based mapping on VPX light objects). Flashers 17-20,28 use SolModCallback for PWM dimming. Coils 51-55 are remapped flashers (PinMAME numbering for WPC lamp matrix columns 7-8). Clock mechanism coils (56-58/42-44 real) are commented out. Gumball release (coil 59) is a PinMAME hack, commented out as unreliable with SolModCallbacks.

## Unresolved questions

- Is the I/O enumeration complete for every supported physical/controller variant?
- Which inferred VPX behaviors reflect real hardware, and which are table-script conveniences?
- Are all mechanism home states, sensors, motion constraints, and ball interactions documented?

## Sources

- `legacy.game.tz`: `games/tz.json` at the pinned migration revision.
