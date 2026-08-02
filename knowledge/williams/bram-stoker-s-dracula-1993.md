# Bram Stoker's Dracula

Coverage: **partial - source-derived recreation knowledge requiring validation**

## Overview

Legacy evidence identifies this candidate as Williams (1993). The information below is preserved for recreation work but is not automatically treated as validated physical-machine fact.

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
- `games/drac.json#/switches/0._vbscript_name`: vpmNudge.TiltSwitch
- `games/drac.json#/switches/0._inferred_type`: cabinet
- `games/drac.json#/switches/0._note`: Set via vpmNudge.TiltSwitch = 14
- `games/drac.json#/switches/1._vbscript_name`: sw15
- `games/drac.json#/switches/1._inferred_type`: drop_target
- `games/drac.json#/switches/1._note`: 3-bank drop target, DTRaise/DTDrop/DTHit via sw15
- `games/drac.json#/switches/2._vbscript_name`: sw16
- `games/drac.json#/switches/2._inferred_type`: rollover
- `games/drac.json#/switches/3._vbscript_name`: sw17
- `games/drac.json#/switches/3._inferred_type`: rollover
- `games/drac.json#/switches/4._vbscript_name`: Controller.Switch(22)
- `games/drac.json#/switches/4._inferred_type`: cabinet
- `games/drac.json#/switches/4._note`: Set to 1 at init -- close coin door
- `games/drac.json#/switches/5._vbscript_name`: Controller.Switch(24)
- `games/drac.json#/switches/5._inferred_type`: cabinet
- `games/drac.json#/switches/5._note`: Set to 1 at init -- keep coin door closed
- `games/drac.json#/switches/6._vbscript_name`: sw25
- `games/drac.json#/switches/6._inferred_type`: rollover
- `games/drac.json#/switches/7._vbscript_name`: sw26
- `games/drac.json#/switches/7._inferred_type`: rollover
- `games/drac.json#/switches/8._vbscript_name`: sw27
- `games/drac.json#/switches/8._inferred_type`: rollover
- `games/drac.json#/switches/9._vbscript_name`: sw28
- `games/drac.json#/switches/9._inferred_type`: rollover
- `games/drac.json#/switches/9._note`: Triggers WireRampOff on hit
- `games/drac.json#/switches/10._vbscript_name`: sw31
- `games/drac.json#/switches/10._inferred_type`: rollover
- `games/drac.json#/switches/11._vbscript_name`: Controller.Switch(34)
- `games/drac.json#/switches/11._inferred_type`: cabinet
- `games/drac.json#/switches/11._note`: Set via PlungerKey keypress
- `games/drac.json#/switches/12._vbscript_name`: sw35
- `games/drac.json#/switches/12._inferred_type`: rollover
- `games/drac.json#/switches/13._vbscript_name`: sw36
- `games/drac.json#/switches/13._inferred_type`: rollover
- `games/drac.json#/switches/13._note`: Triggers leftInlaneSpeedLimit
- `games/drac.json#/switches/14._vbscript_name`: sw37
- `games/drac.json#/switches/14._inferred_type`: rollover
- `games/drac.json#/switches/14._note`: Triggers rightInlaneSpeedLimit
- `games/drac.json#/switches/15._vbscript_name`: sw38
- `games/drac.json#/switches/15._inferred_type`: rollover
- `games/drac.json#/switches/16._vbscript_name`: sw41
- `games/drac.json#/switches/16._inferred_type`: trough
- `games/drac.json#/switches/17._vbscript_name`: sw42
- `games/drac.json#/switches/17._inferred_type`: trough
- `games/drac.json#/switches/18._vbscript_name`: sw43
- `games/drac.json#/switches/18._inferred_type`: trough
- `games/drac.json#/switches/19._vbscript_name`: sw44
- `games/drac.json#/switches/19._inferred_type`: trough
- `games/drac.json#/switches/20._vbscript_name`: sw48
- `games/drac.json#/switches/20._inferred_type`: drain
- `games/drac.json#/switches/20._note`: Ball kicked to trough after 500ms delay
- `games/drac.json#/switches/21._vbscript_name`: sw51
- `games/drac.json#/switches/21._inferred_type`: rollover
- `games/drac.json#/switches/22._vbscript_name`: sw52
- `games/drac.json#/switches/22._inferred_type`: rollover
- `games/drac.json#/switches/23._vbscript_name`: sw53
- `games/drac.json#/switches/23._inferred_type`: kicker
- `games/drac.json#/switches/23._note`: Castle Lock 1 -- triggers WireRampOff on unhit
- `games/drac.json#/switches/24._vbscript_name`: sw54
- `games/drac.json#/switches/24._inferred_type`: kicker
- `games/drac.json#/switches/25._vbscript_name`: sw55
- `games/drac.json#/switches/25._inferred_type`: vuk
- `games/drac.json#/switches/25._note`: VUK -- WirerampPopper fires via SolCallback(6)
- `games/drac.json#/switches/26._vbscript_name`: sw56
- `games/drac.json#/switches/26._inferred_type`: vuk
- `games/drac.json#/switches/26._note`: VUK -- CryptPopper fires via SolCallback(5), removes magnet ball
- `games/drac.json#/switches/27._vbscript_name`: sw57
- `games/drac.json#/switches/27._inferred_type`: kicker
- `games/drac.json#/switches/28._vbscript_name`: sw58
- `games/drac.json#/switches/28._inferred_type`: rollover
- `games/drac.json#/switches/28._note`: Uses vpmTimer.PulseSw (momentary)
- `games/drac.json#/switches/29._vbscript_name`: Bumper2
- `games/drac.json#/switches/29._inferred_type`: bumper
- `games/drac.json#/switches/29._note`: vpmTimer.PulseSw 61
- `games/drac.json#/switches/30._vbscript_name`: Bumper3
- `games/drac.json#/switches/30._inferred_type`: bumper
- `games/drac.json#/switches/30._note`: vpmTimer.PulseSw 62
- `games/drac.json#/switches/31._vbscript_name`: Bumper1
- `games/drac.json#/switches/31._inferred_type`: bumper
- `games/drac.json#/switches/31._note`: vpmTimer.PulseSw 63
- `games/drac.json#/switches/32._vbscript_name`: LeftSlingShot
- `games/drac.json#/switches/32._inferred_type`: slingshot
- `games/drac.json#/switches/32._note`: vpmTimer.PulseSw 64
- `games/drac.json#/switches/33._vbscript_name`: RightSlingShot
- `games/drac.json#/switches/33._inferred_type`: slingshot
- `games/drac.json#/switches/33._note`: vpmTimer.PulseSw 65
- `games/drac.json#/switches/34._vbscript_name`: sw66
- `games/drac.json#/switches/34._inferred_type`: standup_target
- `games/drac.json#/switches/35._vbscript_name`: sw67
- `games/drac.json#/switches/35._inferred_type`: standup_target
- `games/drac.json#/switches/36._vbscript_name`: sw68
- `games/drac.json#/switches/36._inferred_type`: standup_target
- `games/drac.json#/switches/37._vbscript_name`: sw71
- `games/drac.json#/switches/37._inferred_type`: vuk
- `games/drac.json#/switches/37._note`: VUK -- CastlePopper fires via SolCallback(3), removes magnet ball
- `games/drac.json#/switches/38._vbscript_name`: sw72
- `games/drac.json#/switches/38._inferred_type`: vuk
- `games/drac.json#/switches/38._note`: VUK -- CoffinPopper fires via SolCallback(2)
- `games/drac.json#/switches/39._vbscript_name`: sw73
- `games/drac.json#/switches/39._inferred_type`: rollover
- `games/drac.json#/switches/40._vbscript_name`: Controller.Switch(77)
- `games/drac.json#/switches/40._inferred_type`: opto
- `games/drac.json#/switches/40._note`: Set by SolRRampUp/SolRRampDown, tracks moving ramp position
- `games/drac.json#/switches/41._vbscript_name`: Controller.Switch(81)
- `games/drac.json#/switches/41._inferred_type`: opto
- `games/drac.json#/switches/41._note`: MagnetPos > 490 (mist motor at right end)
- `games/drac.json#/switches/42._vbscript_name`: Controller.Switch(82)
- `games/drac.json#/switches/42._inferred_type`: opto
- `games/drac.json#/switches/42._note`: Ball crossing mist magnet line detected in MistTimer
- `games/drac.json#/switches/43._vbscript_name`: Controller.Switch(83)
- `games/drac.json#/switches/43._inferred_type`: opto
- `games/drac.json#/switches/43._note`: MagnetPos < 10 (mist motor at left end)
- `games/drac.json#/switches/44._vbscript_name`: sw84
- `games/drac.json#/switches/44._inferred_type`: rollover
- `games/drac.json#/switches/45._vbscript_name`: sw85
- `games/drac.json#/switches/45._inferred_type`: rollover
- `games/drac.json#/switches/45._note`: Triggers WireRampOff on hit
- `games/drac.json#/switches/46._vbscript_name`: sw86
- `games/drac.json#/switches/46._inferred_type`: standup_target
- `games/drac.json#/switches/47._vbscript_name`: sw87
- `games/drac.json#/switches/47._inferred_type`: standup_target
- `games/drac.json#/switches/48._vbscript_name`: sw88
- `games/drac.json#/switches/48._inferred_type`: standup_target
- `games/drac.json#/coils/0._vbscript_name`: AutoPlunger
- `games/drac.json#/coils/0._vbscript_callback`: SolCallback(1) = "AutoPlunger"
- `games/drac.json#/coils/0._inferred_type`: plunger
- `games/drac.json#/coils/1._vbscript_name`: CoffinPopper
- `games/drac.json#/coils/1._vbscript_callback`: SolCallback(2) = "CoffinPopper"
- `games/drac.json#/coils/1._inferred_type`: vuk
- `games/drac.json#/coils/2._vbscript_name`: CastlePopper
- `games/drac.json#/coils/2._vbscript_callback`: SolCallback(3) = "CastlePopper"
- `games/drac.json#/coils/2._inferred_type`: vuk
- `games/drac.json#/coils/3._vbscript_name`: SolRRampDown
- `games/drac.json#/coils/3._vbscript_callback`: SolCallback(4) = "SolRRampDown"
- `games/drac.json#/coils/3._inferred_type`: diverter
- `games/drac.json#/coils/4._vbscript_name`: CryptPopper
- `games/drac.json#/coils/4._vbscript_callback`: SolCallback(5) = "CryptPopper"
- `games/drac.json#/coils/4._inferred_type`: vuk
- `games/drac.json#/coils/5._vbscript_name`: WirerampPopper
- `games/drac.json#/coils/5._vbscript_callback`: SolCallback(6) = "WirerampPopper"
- `games/drac.json#/coils/5._inferred_type`: vuk
- `games/drac.json#/coils/6._vbscript_name`: SolKnocker
- `games/drac.json#/coils/6._vbscript_callback`: SolCallback(7) = "SolKnocker"
- `games/drac.json#/coils/6._inferred_type`: knocker
- `games/drac.json#/coils/7._vbscript_name`: SolShooterRamp
- `games/drac.json#/coils/7._vbscript_callback`: SolCallback(8) = "SolShooterRamp"
- `games/drac.json#/coils/7._inferred_type`: diverter
- `games/drac.json#/coils/7._note`: Controls sramp2 collidable and FLRamp rotation
- `games/drac.json#/coils/8._vbscript_name`: SolRRampUp
- `games/drac.json#/coils/8._vbscript_callback`: SolCallback(14) = "SolRRampUp"
- `games/drac.json#/coils/8._inferred_type`: diverter
- `games/drac.json#/coils/8._note`: Raises right ramp, sets sw77=True
- `games/drac.json#/coils/9._vbscript_name`: SolRelease
- `games/drac.json#/coils/9._vbscript_callback`: SolCallback(16) = "SolRelease"
- `games/drac.json#/coils/9._inferred_type`: trough_eject
- `games/drac.json#/coils/10._vbscript_name`: Flasher17
- `games/drac.json#/coils/10._vbscript_callback`: SolModCallback(17) = "Flasher17"
- `games/drac.json#/coils/10._inferred_type`: flasher
- `games/drac.json#/coils/10._note`: Top Right Corner Flasher (#906), Dracula Flasher (x2) (#906)
- `games/drac.json#/coils/11._vbscript_name`: Flasher18
- `games/drac.json#/coils/11._vbscript_callback`: SolModCallback(18) = "Flasher18"
- `games/drac.json#/coils/11._inferred_type`: flasher
- `games/drac.json#/coils/11._note`: Jackpot Flasher (#906), Stoker Flasher (#906)
- `games/drac.json#/coils/12._vbscript_name`: Flasher19
- `games/drac.json#/coils/12._vbscript_callback`: SolModCallback(19) = "Flasher19"
- `games/drac.json#/coils/12._inferred_type`: flasher
- `games/drac.json#/coils/12._note`: 3 Bank Flasher (#89), House Flasher (#906)
- `games/drac.json#/coils/13._vbscript_name`: Flasher20
- `games/drac.json#/coils/13._vbscript_callback`: SolModCallback(20) = "Flasher20"
- `games/drac.json#/coils/13._inferred_type`: flasher
- `games/drac.json#/coils/13._note`: Top Left Corner Flasher (#89, #906), Mina Flasher (#906)
- `games/drac.json#/coils/14._vbscript_name`: Flasher21
- `games/drac.json#/coils/14._vbscript_callback`: SolModCallback(21) = "Flasher21"
- `games/drac.json#/coils/14._inferred_type`: flasher
- `games/drac.json#/coils/14._note`: Castle Flasher (#89), Helsing Flasher (#906)
- `games/drac.json#/coils/15._vbscript_name`: Flasher22
- `games/drac.json#/coils/15._vbscript_callback`: SolModCallback(22) = "Flasher22"
- `games/drac.json#/coils/15._inferred_type`: flasher
- `games/drac.json#/coils/15._note`: Left Ramp Flasher (#906), Left Logo Flasher (#906)
- `games/drac.json#/coils/16._vbscript_name`: Flasher23
- `games/drac.json#/coils/16._vbscript_callback`: SolModCallback(23) = "Flasher23"
- `games/drac.json#/coils/16._inferred_type`: flasher
- `games/drac.json#/coils/16._note`: Right Ramp Flasher (#906), Right Logo Flasher (#906)
- `games/drac.json#/coils/17._vbscript_name`: Flasher24
- `games/drac.json#/coils/17._vbscript_callback`: SolModCallback(24) = "Flasher24"
- `games/drac.json#/coils/17._inferred_type`: flasher
- `games/drac.json#/coils/17._note`: Asylum Flasher (#89), Renfield Flasher (#906)
- `games/drac.json#/coils/18._vbscript_name`: SolDTUp
- `games/drac.json#/coils/18._vbscript_callback`: SolCallback(25) = "SolDTUp"
- `games/drac.json#/coils/18._inferred_type`: drop_target_reset
- `games/drac.json#/coils/18._note`: Resets sw15 drop target bank via DTRaise
- `games/drac.json#/coils/19._vbscript_name`: Flasher26
- `games/drac.json#/coils/19._vbscript_callback`: SolModCallback(26) = "Flasher26"
- `games/drac.json#/coils/19._inferred_type`: flasher
- `games/drac.json#/coils/19._note`: Speaker panel flasher
- `games/drac.json#/coils/20._vbscript_name`: SolMistMagnet
- `games/drac.json#/coils/20._vbscript_callback`: SolCallback(27) = "SolMistMagnet"
- `games/drac.json#/coils/20._inferred_type`: magnet
- `games/drac.json#/coils/20._note`: Controls mist multiball magnet attract
- `games/drac.json#/coils/21._vbscript_name`: Controller.Solenoid(28)
- `games/drac.json#/coils/21._inferred_type`: motor
- `games/drac.json#/coils/21._note`: Read directly by MotorTimer_Timer -- no SolCallback, drives mist motor position
- `games/drac.json#/coils/22._vbscript_name`: solTopDiverter
- `games/drac.json#/coils/22._vbscript_callback`: SolCallback(33) = "solTopDiverter"
- `games/drac.json#/coils/22._inferred_type`: diverter
- `games/drac.json#/coils/23._vbscript_name`: SolRGate
- `games/drac.json#/coils/23._vbscript_callback`: SolCallback(34) = "SolRGate"
- `games/drac.json#/coils/23._inferred_type`: gate
- `games/drac.json#/coils/24._vbscript_name`: CastleLockPost
- `games/drac.json#/coils/24._vbscript_callback`: SolCallback(35) = "CastleLockPost"
- `games/drac.json#/coils/24._inferred_type`: post
- `games/drac.json#/coils/24._note`: Castle Lock Post -- controls clpost.isdropped
- `games/drac.json#/coils/25._vbscript_name`: SolLGate
- `games/drac.json#/coils/25._vbscript_callback`: SolCallback(36) = "SolLGate"
- `games/drac.json#/coils/25._inferred_type`: gate
- `games/drac.json#/coils/26`: Unbound legacy outputs record `sLLFlipper` was retained as a migration note only.
- `games/drac.json#/coils/26._vbscript_name`: SolLFlipper
- `games/drac.json#/coils/26._vbscript_callback`: SolCallback(sLLFlipper) = "SolLFlipper"
- `games/drac.json#/coils/26._inferred_type`: flipper
- `games/drac.json#/coils/26._note`: sLLFlipper is a WPC.VBS framework constant (typically 34 for WPC, but varies)
- `games/drac.json#/coils/27`: Unbound legacy outputs record `sLRFlipper` was retained as a migration note only.
- `games/drac.json#/coils/27._vbscript_name`: SolRFlipper
- `games/drac.json#/coils/27._vbscript_callback`: SolCallback(sLRFlipper) = "SolRFlipper"
- `games/drac.json#/coils/27._inferred_type`: flipper
- `games/drac.json#/coils/27._note`: sLRFlipper is a WPC.VBS framework constant (typically 36 for WPC, but varies)
- `games/drac.json#/lamps/0._note`: VLM lightmap LM_L_l16
- `games/drac.json#/lamps/1._note`: VLM lightmap LM_L_l17
- `games/drac.json#/lamps/2._note`: VLM lightmap LM_L_l18
- `games/drac.json#/lamps/3._note`: VLM lightmap LM_L_l21
- `games/drac.json#/lamps/4._note`: VLM lightmap LM_L_l22
- `games/drac.json#/lamps/5._note`: VLM lightmap LM_L_l23
- `games/drac.json#/lamps/6._note`: VLM lightmap LM_L_l24
- `games/drac.json#/lamps/7._note`: VLM lightmap LM_L_l25
- `games/drac.json#/lamps/8._note`: VLM lightmap LM_L_l26
- `games/drac.json#/lamps/9._note`: VLM lightmap LM_L_l27
- `games/drac.json#/lamps/10._note`: VLM lightmap LM_L_l28
- `games/drac.json#/lamps/11._note`: VLM lightmap LM_L_l31
- `games/drac.json#/lamps/12._note`: VLM lightmap LM_L_l32
- `games/drac.json#/lamps/13._note`: VLM lightmap LM_L_l33
- `games/drac.json#/lamps/14._note`: VLM lightmap LM_L_l34
- `games/drac.json#/lamps/15._note`: VLM lightmap LM_L_l35
- `games/drac.json#/lamps/16._note`: VLM lightmap LM_L_l36
- `games/drac.json#/lamps/17._note`: VLM lightmap LM_L_l37
- `games/drac.json#/lamps/18._note`: VLM lightmap LM_L_l38
- `games/drac.json#/lamps/19._note`: VLM lightmap LM_L_l41
- `games/drac.json#/lamps/20._note`: VLM lightmap LM_L_l42
- `games/drac.json#/lamps/21._note`: VLM lightmap LM_L_l43
- `games/drac.json#/lamps/22._note`: VLM lightmap LM_L_l44
- `games/drac.json#/lamps/23._note`: VLM lightmap LM_L_l45
- `games/drac.json#/lamps/24._note`: VLM lightmap LM_L_l46
- `games/drac.json#/lamps/25._note`: VLM lightmap LM_L_l47
- `games/drac.json#/lamps/26._note`: VLM lightmap LM_L_l48
- `games/drac.json#/lamps/27._note`: VLM lightmap LM_L_l51
- `games/drac.json#/lamps/28._note`: VLM lightmap LM_L_l52
- `games/drac.json#/lamps/29._note`: VLM lightmap LM_L_l54
- `games/drac.json#/lamps/30._note`: VLM lightmap LM_L_l55
- `games/drac.json#/lamps/31._note`: VLM lightmap LM_L_l56
- `games/drac.json#/lamps/32._note`: VLM lightmap LM_L_l57
- `games/drac.json#/lamps/33._note`: VLM lightmap LM_L_l58
- `games/drac.json#/lamps/34._note`: VLM lightmap LM_L_L61
- `games/drac.json#/lamps/35._note`: VLM lightmap LM_L_L62
- `games/drac.json#/lamps/36._note`: VLM lightmap LM_L_L63
- `games/drac.json#/lamps/37._note`: VLM lightmap LM_L_l64
- `games/drac.json#/lamps/38._note`: VLM lightmap LM_L_l65
- `games/drac.json#/lamps/39._note`: VLM lightmap LM_L_l66
- `games/drac.json#/lamps/40._note`: VLM lightmap LM_L_l67
- `games/drac.json#/lamps/41._note`: VLM lightmap LM_L_L68
- `games/drac.json#/lamps/42._note`: VLM lightmap LM_L_l71
- `games/drac.json#/lamps/43._note`: VLM lightmap LM_L_l72
- `games/drac.json#/lamps/44._note`: VLM lightmap LM_L_l73
- `games/drac.json#/lamps/45._note`: VLM lightmap LM_L_l74
- `games/drac.json#/lamps/46._note`: VLM lightmap LM_L_l75
- `games/drac.json#/lamps/47._note`: VLM lightmap LM_L_l76
- `games/drac.json#/lamps/48._note`: VLM lightmap LM_L_l77
- `games/drac.json#/lamps/49._note`: VLM lightmap LM_L_l78
- `games/drac.json#/lamps/50._note`: VLM lightmap LM_L_l81
- `games/drac.json#/lamps/51._note`: VLM lightmap LM_L_l82
- `games/drac.json#/lamps/52._note`: VLM lightmap LM_L_l83
- `games/drac.json#/lamps/53._note`: VLM lightmap LM_L_l84
- `games/drac.json#/lamps/54._note`: VLM lightmap LM_L_l85
- `games/drac.json#/lamps/55._note`: VLM lightmap LM_L_l86
- `games/drac.json#/lamps/56`: Unbound legacy outputs record `ml1` was retained as a migration note only.
- `games/drac.json#/lamps/56._inferred_type`: mist_lamp
- `games/drac.json#/lamps/56._note`: Controlled by MotorTimer_Timer based on magnet position, not ROM-driven
- `games/drac.json#/lamps/57`: Unbound legacy outputs record `ml2` was retained as a migration note only.
- `games/drac.json#/lamps/57._inferred_type`: mist_lamp
- `games/drac.json#/lamps/57._note`: Script-controlled mist position indicator
- `games/drac.json#/lamps/58`: Unbound legacy outputs record `ml3` was retained as a migration note only.
- `games/drac.json#/lamps/58._inferred_type`: mist_lamp
- `games/drac.json#/lamps/58._note`: Script-controlled mist position indicator
- `games/drac.json#/lamps/59`: Unbound legacy outputs record `ml4` was retained as a migration note only.
- `games/drac.json#/lamps/59._inferred_type`: mist_lamp
- `games/drac.json#/lamps/59._note`: Script-controlled mist position indicator
- `games/drac.json#/lamps/60`: Unbound legacy outputs record `ml5` was retained as a migration note only.
- `games/drac.json#/lamps/60._inferred_type`: mist_lamp
- `games/drac.json#/lamps/60._note`: Script-controlled mist position indicator
- `games/drac.json#/lamps/61`: Unbound legacy outputs record `ml6` was retained as a migration note only.
- `games/drac.json#/lamps/61._inferred_type`: mist_lamp
- `games/drac.json#/lamps/61._note`: Script-controlled mist position indicator
- `games/drac.json#/lamps/62`: Unbound legacy outputs record `ml7` was retained as a migration note only.
- `games/drac.json#/lamps/62._inferred_type`: mist_lamp
- `games/drac.json#/lamps/62._note`: Script-controlled mist position indicator
- `games/drac.json#/lamps/63`: Unbound legacy outputs record `ml8` was retained as a migration note only.
- `games/drac.json#/lamps/63._inferred_type`: mist_lamp
- `games/drac.json#/lamps/63._note`: Script-controlled mist position indicator
- `games/drac.json#/lamps/64`: Unbound legacy outputs record `ml9` was retained as a migration note only.
- `games/drac.json#/lamps/64._inferred_type`: mist_lamp
- `games/drac.json#/lamps/64._note`: Script-controlled mist position indicator
- `games/drac.json#/lamps/65`: Unbound legacy outputs record `ml10` was retained as a migration note only.
- `games/drac.json#/lamps/65._inferred_type`: mist_lamp
- `games/drac.json#/lamps/65._note`: Script-controlled mist position indicator
- `games/drac.json#/lamps/66`: Unbound legacy outputs record `ml11` was retained as a migration note only.
- `games/drac.json#/lamps/66._inferred_type`: mist_lamp
- `games/drac.json#/lamps/66._note`: Script-controlled mist position indicator
- `games/drac.json#/lamps/67`: Unbound legacy outputs record `ml12` was retained as a migration note only.
- `games/drac.json#/lamps/67._inferred_type`: mist_lamp
- `games/drac.json#/lamps/67._note`: Script-controlled mist position indicator
- `games/drac.json#/lamps/68`: Unbound legacy outputs record `ml13` was retained as a migration note only.
- `games/drac.json#/lamps/68._inferred_type`: mist_lamp
- `games/drac.json#/lamps/68._note`: Script-controlled mist position indicator
- `games/drac.json#/_source/confidence_notes`: High confidence on switches and coils from direct VBScript parsing. Lamp numbers inferred from VLM lightmap array names (LM_L_lNN) and mist lamp objects (ml1-ml13). No explicit Const sw* or Const s* declarations found in table script; switch/coil numbers are hardcoded in Controller.Switch() calls and SolCallback() assignments. Flipper solenoid IDs (sLRFlipper, sLLFlipper) come from WPC.VBS framework. AllLamps collection defined in VPX editor, not script.

## Unresolved questions

- Is the I/O enumeration complete for every supported physical/controller variant?
- Which inferred VPX behaviors reflect real hardware, and which are table-script conveniences?
- Are all mechanism home states, sensors, motion constraints, and ball interactions documented?

## Sources

- `legacy.game.drac`: `games/drac.json` at the pinned migration revision.
