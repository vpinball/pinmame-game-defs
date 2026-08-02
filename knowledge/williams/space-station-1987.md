# Space Station

Coverage: **partial - source-derived recreation knowledge requiring validation**

## Overview

Legacy evidence identifies this candidate as Williams (1987). The information below is preserved for recreation work but is not automatically treated as validated physical-machine fact.

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

- `games/space-station.json#/switches/0._note`: Controller.Switch(3) set to 0 on StartGameKey release in Table1_KeyUp. System 11 start button.
- `games/space-station.json#/switches/1._note`: vpmNudge.TiltSwitch = 9. Tilt bob switch.
- `games/space-station.json#/switches/2._note`: sw10_Hit/UnHit sets Controller.Switch(10). Ball drains here, then SolTrough (sol 1) kicks from sw10 into trough. Plays RandomSoundDrain on hit.
- `games/space-station.json#/switches/3._note`: sw11_Hit/UnHit sets Controller.Switch(11). Forced ON at init. SolRelease (sol 2) kicks from sw11 to shooter lane. Nearest to ball eject.
- `games/space-station.json#/switches/4._note`: sw12_Hit/UnHit sets Controller.Switch(12). Forced ON at init. UpdateTrough cascades: if sw11 empty, kicks from sw12.
- `games/space-station.json#/switches/5._note`: sw13_Hit/UnHit sets Controller.Switch(13). Forced ON at init. UpdateTrough cascades: if sw12 empty, kicks from sw13.
- `games/space-station.json#/switches/6._note`: Controller.Switch(14) on/off. Comment says 'Upper Playfield'. One of three upper playfield rollovers.
- `games/space-station.json#/switches/7._note`: Controller.Switch(15) on/off. Comment says 'Upper Playfield'. Second upper playfield rollover.
- `games/space-station.json#/switches/8._note`: Controller.Switch(16) on/off. Comment says 'Upper Playfield'. Third upper playfield rollover.
- `games/space-station.json#/switches/9._note`: Controller.Switch(17) on/off. Comment says 'Left Inlane'. Plays RandomSoundOutlaneRollover on hit.
- `games/space-station.json#/switches/10._note`: STHit 18. First letter 'S' of SHUTTLE standup target bank. Part of 7-target SHUTTLE group (sw18-24).
- `games/space-station.json#/switches/11._note`: STHit 19. Letter 'H' of SHUTTLE standup target bank.
- `games/space-station.json#/switches/12._note`: STHit 20. Letter 'U' of SHUTTLE standup target bank.
- `games/space-station.json#/switches/13._note`: STHit 21. First letter 'T' of SHUTTLE standup target bank.
- `games/space-station.json#/switches/14._note`: STHit 22. Second letter 'T' of SHUTTLE standup target bank.
- `games/space-station.json#/switches/15._note`: STHit 23. Letter 'L' of SHUTTLE standup target bank.
- `games/space-station.json#/switches/16._note`: STHit 24. Letter 'E' of SHUTTLE standup target bank.
- `games/space-station.json#/switches/17._note`: STHit 25. Letter 'S' of STA(TION) standup target group (sw25-27).
- `games/space-station.json#/switches/18._note`: STHit 26. Letter 'T' of STA standup target group.
- `games/space-station.json#/switches/19._note`: STHit 27. Letter 'A' of STA standup target group.
- `games/space-station.json#/switches/20._note`: STHit 28. Letter 'T' of TION standup target group (sw28-31).
- `games/space-station.json#/switches/21._note`: STHit 29. Letter 'I' of TION standup target group.
- `games/space-station.json#/switches/22._note`: STHit 30. Letter 'O' of TION standup target group.
- `games/space-station.json#/switches/23._note`: STHit 31. Letter 'N' of TION standup target group.
- `games/space-station.json#/switches/24._note`: Controller.Switch(32) on/off. Comment says 'Right Inlane'. Plays RandomSoundOutlaneRollover on hit.
- `games/space-station.json#/switches/25._note`: DTHit 33. Single drop target. Reset by sol 8 (ResetDrops1). TargetBouncer applied on hit.
- `games/space-station.json#/switches/26._note`: STHit 35. Comment says 'Change'. Standalone standup target.
- `games/space-station.json#/switches/27._note`: Controller.Switch(37) on/off. Comment says 'Left Orbit'. Rollunder switch.
- `games/space-station.json#/switches/28._note`: Controller.Switch(38) on/off. Comment says 'USA Rollover'. Part of 3-rollover USA group (sw38-40).
- `games/space-station.json#/switches/29._note`: Controller.Switch(39) on/off. Comment says 'USA Rollover'. Second of USA group.
- `games/space-station.json#/switches/30._note`: Controller.Switch(40) on/off. Comment says 'USA Rollover'. Third of USA group.
- `games/space-station.json#/switches/31._note`: Controller.Switch(41) on/off. Upper left VUK. Ball captured on hit (KickerBall41), ejected by sol 3 (KickerUpperLeft). WireRampOn False called on entry.
- `games/space-station.json#/switches/32._note`: Controller.Switch(42) on/off. Upper right VUK. Ball captured on hit (KickerBall42), ejected by sol 4 (KickerUpperRight). WireRampOn False called on entry.
- `games/space-station.json#/switches/33._note`: Controller.Switch(43) on/off. Sets BIPL (Ball In Plunger Lane) flag on hit. Used to determine plunger release sound.
- `games/space-station.json#/switches/34._note`: Controller.Switch(45) on/off. Right dock kicker. Ball captured on hit (KickerBall45), ejected by sol 17 (RightDockKick). Has sw45_Animate sub for visual animation.
- `games/space-station.json#/switches/35._note`: Controller.Switch(46) on/off. Comment says 'Right Lock Ramp Entry'.
- `games/space-station.json#/switches/36._note`: Controller.Switch(47) on/off. Left dock kicker. Ball captured on hit (KickerBall47), ejected by sol 32 (LeftDockKick). WireRampOff called on entry.
- `games/space-station.json#/switches/37._note`: Controller.Switch(48) on/off. Comment says 'Left Lock Entry'. Rollunder switch.
- `games/space-station.json#/switches/38._note`: PulseSw 50. Comment says 'Lower Right Rubber Switch'. Triggered by rubber hit event.
- `games/space-station.json#/switches/39._note`: Set by MotorUpdate(): Controller.Switch(52)=1 when MotorPos>180, else 0. Tracks position of rotating space station toy. NOT a physical VPX switch -- driven by motor code.
- `games/space-station.json#/switches/40._note`: Set by MotorUpdate(): Controller.Switch(53)=1 when MotorPos between 90 and 270, else 0. Tracks position of rotating space station toy. NOT a physical VPX switch -- driven by motor code.
- `games/space-station.json#/switches/41._note`: PulseSw 54. Comment says 'Uppper Right Rubber Switch'. Triggered by rubber hit event.
- `games/space-station.json#/switches/42._note`: DTHit 57. First of 3-bank drop targets (sw57-59). Reset by sol 6 (ResetDrops3).
- `games/space-station.json#/switches/43._note`: DTHit 58. Second of 3-bank drop targets. Reset by sol 6.
- `games/space-station.json#/switches/44._note`: DTHit 59. Third of 3-bank drop targets. Reset by sol 6.
- `games/space-station.json#/switches/45._note`: PulseSw 60. Bumper1_Hit fires PulseSw 60 with RandomSoundBumperTop.
- `games/space-station.json#/switches/46._note`: PulseSw 61. Bumper2_Hit fires PulseSw 61 with RandomSoundBumperMiddle.
- `games/space-station.json#/switches/47._note`: PulseSw 62. Bumper3_Hit fires PulseSw 62 with RandomSoundBumperBottom.
- `games/space-station.json#/switches/48._note`: PulseSw 63. Fired from LeftSlingShot_Slingshot event via LS.VelocityCorrect.
- `games/space-station.json#/switches/49._note`: PulseSw 64. Fired from RightSlingShot_Slingshot event via RS.VelocityCorrect.
- `games/space-station.json#/coils/0._vbscript_callback`: SolTrough
- `games/space-station.json#/coils/0._inferred_type`: ball_management
- `games/space-station.json#/coils/0._note`: SolCallback(1). Kicks ball from drain (sw10) into trough. sw10.kick 57, 10.
- `games/space-station.json#/coils/1._vbscript_callback`: SolRelease
- `games/space-station.json#/coils/1._inferred_type`: ball_management
- `games/space-station.json#/coils/1._note`: SolCallback(2). Kicks ball from trough position 3 (sw11) to shooter lane. sw11.kick 57, 10.
- `games/space-station.json#/coils/2._vbscript_callback`: KickerUpperLeft
- `games/space-station.json#/coils/2._inferred_type`: ball_management
- `games/space-station.json#/coils/2._note`: SolCallback(3). Ejects ball from upper left VUK (sw41). KickBall angle 0, velz 30, zlift 10.
- `games/space-station.json#/coils/3._vbscript_callback`: KickerUpperRight
- `games/space-station.json#/coils/3._inferred_type`: ball_management
- `games/space-station.json#/coils/3._note`: SolCallback(4). Ejects ball from upper right VUK (sw42). KickBall angle 270, velz 60, zlift 10.
- `games/space-station.json#/coils/4._vbscript_callback`: ResetDrops3
- `games/space-station.json#/coils/4._inferred_type`: drop_target_reset
- `games/space-station.json#/coils/4._note`: SolCallback(6). Raises 3-bank drop targets sw57, sw58, sw59 via DTRaise.
- `games/space-station.json#/coils/5._vbscript_callback`: SolKnocker
- `games/space-station.json#/coils/5._inferred_type`: knocker
- `games/space-station.json#/coils/5._note`: SolCallback(7). Cabinet knocker solenoid. Fires KnockerSolenoid sub.
- `games/space-station.json#/coils/6._vbscript_callback`: ResetDrops1
- `games/space-station.json#/coils/6._inferred_type`: drop_target_reset
- `games/space-station.json#/coils/6._note`: SolCallback(8). Raises single drop target sw33 via DTRaise.
- `games/space-station.json#/coils/7._vbscript_callback`: GIUpdates
- `games/space-station.json#/coils/7._inferred_type`: gi_lighting
- `games/space-station.json#/coils/7._note`: SolModCallback(9). Controls playfield GI brightness level. Uses SolModCallback (receives intensity level, not on/off).
- `games/space-station.json#/coils/8._vbscript_callback`: GiSelect
- `games/space-station.json#/coils/8._inferred_type`: gi_lighting
- `games/space-station.json#/coils/8._note`: SolCallback(10). Selects green GI circuit for playfield.
- `games/space-station.json#/coils/9._vbscript_callback`: GiBackbox
- `games/space-station.json#/coils/9._inferred_type`: gi_lighting
- `games/space-station.json#/coils/9._note`: SolCallback(11). Controls backbox GI. Fires Sound_Solenoid_ACSelect_Relay on state change.
- `games/space-station.json#/coils/10._vbscript_callback`: SolACSelectRelay
- `games/space-station.json#/coils/10._inferred_type`: mechanism
- `games/space-station.json#/coils/10._note`: SolCallback(12). System 11 A/C Select Relay. Switches between A and C lamp columns for doubled lamp matrix capacity. Fires Sound_Solenoid_ACSelect_Relay.
- `games/space-station.json#/coils/11._vbscript_callback`: SolKickBack
- `games/space-station.json#/coils/11._inferred_type`: ball_management
- `games/space-station.json#/coils/11._note`: SolCallback(13). Left kickback. Fires Kickback.Fire on enable, Kickback.PullBack on disable.
- `games/space-station.json#/coils/12._vbscript_callback`: SolMod15
- `games/space-station.json#/coils/12._inferred_type`: flasher
- `games/space-station.json#/coils/12._note`: SolModCallback(15). Playfield top panel flashers. Drives f15, f15b, f15c VPX flasher objects. Comment: '28v Lamps'.
- `games/space-station.json#/coils/13._vbscript_callback`: StationMotor
- `games/space-station.json#/coils/13._inferred_type`: mechanism
- `games/space-station.json#/coils/13._note`: SolCallback(16). Controls rotating space station toy motor. Custom motor code (not cvpmMech) -- MotorUpdate() runs on main timer, increments MotorPos 0-360 degrees. Motor drives sw52 and sw53 position switches and UpdateUFO visual animation with 4-position diverter logic.
- `games/space-station.json#/coils/14._vbscript_callback`: RightDockKick
- `games/space-station.json#/coils/14._inferred_type`: ball_management
- `games/space-station.json#/coils/14._note`: SolCallback(17). Ejects ball from right dock VUK (sw45). KickBall angle 0, random vel 16-24.
- `games/space-station.json#/coils/15._vbscript_callback`: SolMod25
- `games/space-station.json#/coils/15._inferred_type`: flasher
- `games/space-station.json#/coils/15._note`: SolModCallback(25). Drives f25, f25b flasher objects. Comment: 'Relaunch (x2 pf) + ON Flashers (x2 Backbox)'.
- `games/space-station.json#/coils/16._vbscript_callback`: SolMod26
- `games/space-station.json#/coils/16._inferred_type`: flasher
- `games/space-station.json#/coils/16._note`: SolModCallback(26). Drives f26, f26b flasher objects. Comment: 'Left Side (x2 pf) + SP Flashers (x2 Backbox)'.
- `games/space-station.json#/coils/17._vbscript_callback`: SolMod27
- `games/space-station.json#/coils/17._inferred_type`: flasher
- `games/space-station.json#/coils/17._note`: SolModCallback(27). Drives f27, f27b flasher objects. Comment: 'Right Side (x2 pf) + AC Flashers (x2 Backbox)'.
- `games/space-station.json#/coils/18._vbscript_callback`: SolMod28
- `games/space-station.json#/coils/18._inferred_type`: flasher
- `games/space-station.json#/coils/18._note`: SolModCallback(28). Drives f28, f28b flasher objects. Comment: 'Top Upper Playfield (x2 pf) + ES Flashers (x2 Backbox)'.
- `games/space-station.json#/coils/19._vbscript_callback`: SolMod29
- `games/space-station.json#/coils/19._inferred_type`: flasher
- `games/space-station.json#/coils/19._note`: SolModCallback(29). Drives f29, f29b flasher objects. Comment: 'Playfield Top Panel (x2pf) + TA Flashers (x2 Backbox)'.
- `games/space-station.json#/coils/20._vbscript_callback`: SolMod30
- `games/space-station.json#/coils/20._inferred_type`: flasher
- `games/space-station.json#/coils/20._note`: SolModCallback(30). Drives f30 flasher object. Comment: 'Flame + TI Flashers (x4 Backbox)'.
- `games/space-station.json#/coils/21._vbscript_callback`: SolMod31
- `games/space-station.json#/coils/21._inferred_type`: flasher
- `games/space-station.json#/coils/21._note`: SolModCallback(31). Drives f31 flasher object. Comment: 'Station Flashers (x2 Backbox)'.
- `games/space-station.json#/coils/22._vbscript_callback`: LeftDockKick
- `games/space-station.json#/coils/22._inferred_type`: ball_management
- `games/space-station.json#/coils/22._note`: SolCallback(32). Ejects ball from left dock VUK (sw47). KickBall angle 0, random vel 16-24. Comment incorrectly says 'Right Dock Kickback' but code clearly operates on sw47/KickerBall47 (left dock).
- `games/space-station.json#/_source/confidence_notes`: High confidence extraction from VPW VBScript. Platform detected as System 11 via LoadVPM call loading 's11.vbs'. ROM identified as 'spstn_l5' from Const cGameName. Trough is a pre-cvpmTrough manual implementation: sw10 is drain (outhole), sw11-sw13 are trough positions with sw13 nearest drain and sw11 nearest shooter. SolTrough (sol 1) kicks from sw10, SolRelease (sol 2) kicks from sw11 to shooter lane. UpdateTrough timer cascades balls from sw13 to sw12 to sw11 using BallCntOver checks. Tilt switch is 9 per vpmNudge.TiltSwitch assignment. Start button is switch 3, handled via StartGameKey in KeyUp (Controller.Switch(3)=0 on release). Space Station toy motor (sol 16) drives a rotating UFO mechanism via MotorPos variable (0-360 degrees). Motor position drives two switches: sw52 is ON when MotorPos>180, sw53 is ON when MotorPos between 90 and 270. This is NOT cvpmMech -- it is custom code in MotorUpdate() called from the main timer. Four VUKs: sw41 (upper left, sol 3), sw42 (upper right, sol 4), sw45 (right dock, sol 17), sw47 (left dock, sol 32). Kickback at sol 13 fires a VPX Kickback object. A/C Select Relay (sol 12) is a System 11 wiring feature. Standup targets spell 'SHUTTLE' (sw18-24), 'STA' (sw25-27), 'TION' (sw28-31), and 'Change' (sw35). Drop targets: sw33 is single drop target (reset by sol 8), sw57-59 are 3-bank drop targets (reset by sol 6). Slingshots are PulseSw 63 (left) and 64 (right). Bumpers are PulseSw 60-62. Rubber switches sw50 and sw54 use PulseSw. Flipper solenoids use framework constants sLRFlipper and sLLFlipper from s11.vbs. Lamps extracted from BL_IN_l* VLM arrays -- IDs 1-64 present with gaps at 37, 41, 46-49, 57. Flashers on SolModCallback: sol 15 (top panel x3), sol 25 (relaunch+ON), sol 26 (left side+SP), sol 27 (right side+AC), sol 28 (upper playfield+ES), sol 29 (top panel+TA), sol 30 (flame+TI), sol 31 (station x2 backbox). GI controlled via SolModCallback 9 (playfield level), sol 10 (green select), sol 11 (backbox). Comment notes sols 18-22 are slings and pop bumpers (handled by VPX physics, not in SolCallback). Sol 5 and 14 explicitly commented as unused.

## Unresolved questions

- Is the I/O enumeration complete for every supported physical/controller variant?
- Which inferred VPX behaviors reflect real hardware, and which are table-script conveniences?
- Are all mechanism home states, sensors, motion constraints, and ball interactions documented?

## Sources

- `legacy.game.space-station`: `games/space-station.json` at the pinned migration revision.
