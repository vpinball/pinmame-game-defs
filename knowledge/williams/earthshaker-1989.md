# Earthshaker

Coverage: **partial - source-derived recreation knowledge requiring validation**

## Overview

Legacy evidence identifies this candidate as Williams (1989). The information below is preserved for recreation work but is not automatically treated as validated physical-machine fact.

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

- `games/esha.json#/switches/0._vbscript_name`: vpmNudge.TiltSwitch
- `games/esha.json#/switches/0._note`: Framework tilt switch, assigned via vpmNudge.TiltSwitch = 9
- `games/esha.json#/switches/2._note`: Ball eject position; ReleaseBall kicks from here
- `games/esha.json#/switches/5._note`: Wire trigger with rightInlaneSpeedLimit handler
- `games/esha.json#/switches/9._note`: Wire trigger with leftInlaneSpeedLimit handler
- `games/esha.json#/switches/10._note`: StandupTarget class instance ST19
- `games/esha.json#/switches/11._note`: Locks ball, kicked by SolCallback(05) VUKLeft
- `games/esha.json#/switches/12._note`: StandupTarget class instance ST21
- `games/esha.json#/switches/13._note`: StandupTarget class instance ST22
- `games/esha.json#/switches/14._note`: StandupTarget class instance ST23
- `games/esha.json#/switches/15._note`: StandupTarget class instance ST24
- `games/esha.json#/switches/16._note`: Set by InstituteTimer — position encoder for Earthquake Institute building elevator motor. ON when at bottom or moving down past 2/3.
- `games/esha.json#/switches/17._note`: Set by InstituteTimer — position encoder for Earthquake Institute building elevator motor. ON when at top or bottom, OFF in middle zone.
- `games/esha.json#/switches/18._note`: Drop target, reset by SolCallback(03) SolDropReset
- `games/esha.json#/switches/19._note`: Drop target, reset by SolCallback(03) SolDropReset
- `games/esha.json#/switches/20._note`: Drop target, reset by SolCallback(03) SolDropReset
- `games/esha.json#/switches/21._note`: StandupTarget class instance ST30
- `games/esha.json#/switches/22._note`: Pulse switch (vpmTimer.pulseSw)
- `games/esha.json#/switches/23._note`: Pulse switch (vpmTimer.pulseSw)
- `games/esha.json#/switches/28._note`: Locks ball, kicked by SolCallback(13) VUKTop
- `games/esha.json#/switches/29._note`: Plays 'Subway' sound on hit
- `games/esha.json#/switches/30._note`: sw39wall collidable set false at init
- `games/esha.json#/switches/31._note`: Locks ball, kicked by SolCallback(06) VUKBot
- `games/esha.json#/switches/32._note`: Pulse switch (vpmTimer.PulseSw)
- `games/esha.json#/switches/33._note`: Virtual switch set by OpenFaultTimer/CloseFaultTimer animation — indicates diverter bridge is fully open (1) or closed (0)
- `games/esha.json#/switches/34._note`: Pulse switch (vpmTimer.pulseSw)
- `games/esha.json#/switches/35._note`: Pulse switch (vpmTimer.pulseSw)
- `games/esha.json#/switches/39._note`: Pulse switch via vpmTimer.PulseSw(52)
- `games/esha.json#/switches/40._note`: Pulse switch via vpmTimer.PulseSw(53)
- `games/esha.json#/switches/41._note`: Pulse switch via vpmTimer.PulseSw(54)
- `games/esha.json#/switches/42._note`: Pulse switch via vpmTimer.PulseSw 55
- `games/esha.json#/switches/43._note`: Pulse switch via vpmTimer.PulseSw 56
- `games/esha.json#/switches/44._note`: Set via Controller.Switch(57) in Table1_KeyDown/KeyUp (RightFlipperKey)
- `games/esha.json#/switches/45._note`: Set via Controller.Switch(58) in Table1_KeyDown/KeyUp (LeftFlipperKey)
- `games/esha.json#/coils/0._vbscript_callback`: SolOuthole
- `games/esha.json#/coils/0._inferred_type`: ball_management
- `games/esha.json#/coils/0._note`: Kicks ball from outhole (sw10) toward trough
- `games/esha.json#/coils/1._vbscript_callback`: ReleaseBall
- `games/esha.json#/coils/1._inferred_type`: ball_management
- `games/esha.json#/coils/1._note`: Kicks ball from trough position 1 (sw11) to shooter lane
- `games/esha.json#/coils/2._vbscript_callback`: SolDropReset
- `games/esha.json#/coils/2._inferred_type`: drop_target_reset
- `games/esha.json#/coils/2._note`: Resets drop targets sw27, sw28, sw29 via DTRaise
- `games/esha.json#/coils/3._vbscript_callback`: SolFault
- `games/esha.json#/coils/3._inferred_type`: diverter
- `games/esha.json#/coils/3._note`: Toggles FaultOpen state; animates diverter bridge via OpenFaultTimer/CloseFaultTimer
- `games/esha.json#/coils/4._vbscript_callback`: VUKLeft
- `games/esha.json#/coils/4._inferred_type`: ball_management
- `games/esha.json#/coils/4._note`: Kicks ball from sw20 saucer (KickBall angle=250, vel=15, velz=5)
- `games/esha.json#/coils/5._vbscript_callback`: VUKBot
- `games/esha.json#/coils/5._inferred_type`: ball_management
- `games/esha.json#/coils/5._note`: Kicks ball from sw40 saucer (KickBall angle=0, vel=0, velz=50)
- `games/esha.json#/coils/6._vbscript_callback`: vpmSolSound SoundFX("Knocker",DOFKnocker),
- `games/esha.json#/coils/6._inferred_type`: sound_effect
- `games/esha.json#/coils/7._vbscript_callback`: InstituteDrop
- `games/esha.json#/coils/7._inferred_type`: motor
- `games/esha.json#/coils/7._note`: Controls Earthquake Institute building elevator motor. Raises/lowers building over 3-second cycle. Position reported via switches 25/26.
- `games/esha.json#/coils/8._vbscript_callback`: PFGI2
- `games/esha.json#/coils/8._inferred_type`: gi
- `games/esha.json#/coils/8._note`: Controls GIU collection (upper playfield general illumination). Inverted: enabled=True turns lights OFF.
- `games/esha.json#/coils/9._vbscript_callback`: Flash112
- `games/esha.json#/coils/9._inferred_type`: flasher
- `games/esha.json#/coils/9._note`: SolModCallBack (PWM). Controls FlBG1-FlBG12 backglass flasher visibility in VR mode.
- `games/esha.json#/coils/10._vbscript_callback`: VUKTop
- `games/esha.json#/coils/10._inferred_type`: ball_management
- `games/esha.json#/coils/10._note`: Kicks ball from sw37 saucer (KickBall angle=0, vel=0, velz=50)
- `games/esha.json#/coils/11._vbscript_callback`: Flash114
- `games/esha.json#/coils/11._inferred_type`: flasher
- `games/esha.json#/coils/11._note`: SolModCallBack (PWM)
- `games/esha.json#/coils/12._vbscript_callback`: PFGI
- `games/esha.json#/coils/12._inferred_type`: gi
- `games/esha.json#/coils/12._note`: Controls GI collection (main playfield general illumination). Inverted: enabled=True turns lights OFF.
- `games/esha.json#/coils/13._vbscript_callback`: Flash116
- `games/esha.json#/coils/13._inferred_type`: flasher
- `games/esha.json#/coils/13._note`: SolModCallBack (PWM). Comment: '16: On Ramp & J Bumper Flasher'
- `games/esha.json#/coils/14._vbscript_callback`: ShakerMotor
- `games/esha.json#/coils/14._inferred_type`: motor
- `games/esha.json#/coils/14._note`: Activates ShakeTimer which applies nudge forces (simulates earthquake shaking)
- `games/esha.json#/coils/15._vbscript_callback`: Flash125
- `games/esha.json#/coils/15._inferred_type`: flasher
- `games/esha.json#/coils/15._note`: SolModCallBack (PWM). Comment: '01C: Captive Ball Flasher'
- `games/esha.json#/coils/16._vbscript_callback`: Flash126
- `games/esha.json#/coils/16._inferred_type`: flasher
- `games/esha.json#/coils/16._note`: SolModCallBack (PWM). Comment: '02C: Center Ramp 1 & Building Flasher'. Also controls FlBG26 backglass flasher.
- `games/esha.json#/coils/17._vbscript_callback`: Flash127
- `games/esha.json#/coils/17._inferred_type`: flasher
- `games/esha.json#/coils/17._note`: SolModCallBack (PWM). Comment: '03C: Center Ramp 2 & Spinner Flasher'. Also controls FlBG27 backglass flasher.
- `games/esha.json#/coils/18._vbscript_callback`: Flash128
- `games/esha.json#/coils/18._inferred_type`: flasher
- `games/esha.json#/coils/18._note`: SolModCallBack (PWM). Comment: '05A: Eject Hole Flasher'. Also controls FlBG28 backglass flasher.
- `games/esha.json#/coils/19._vbscript_callback`: Flash129
- `games/esha.json#/coils/19._inferred_type`: flasher
- `games/esha.json#/coils/19._note`: SolModCallBack (PWM). Comment: '05C: Center Ramp 4 Flasher'
- `games/esha.json#/coils/20._vbscript_callback`: Flash130
- `games/esha.json#/coils/20._inferred_type`: flasher
- `games/esha.json#/coils/20._note`: SolModCallBack (PWM). Comment: '06C: Right Ramp 1 Flasher'. Also controls FlBG30 backglass flasher.
- `games/esha.json#/coils/21._vbscript_callback`: Flash131
- `games/esha.json#/coils/21._inferred_type`: flasher
- `games/esha.json#/coils/21._note`: SolModCallBack (PWM). Comment: '07C: Right Ramp 2 Flasher'. Also controls FlBG31 backglass flasher.
- `games/esha.json#/coils/22._vbscript_callback`: Flash132
- `games/esha.json#/coils/22._inferred_type`: flasher
- `games/esha.json#/coils/22._note`: SolModCallBack (PWM). Controls two flasher objects plus FlBG32 backglass flasher.
- `games/esha.json#/coils/23._vbscript_callback`: SolRFlipper
- `games/esha.json#/coils/23._inferred_type`: flipper
- `games/esha.json#/coils/23._note`: Framework constant sLRFlipper=46 from core.vbs/S11.VBS
- `games/esha.json#/coils/24._vbscript_callback`: SolLFlipper
- `games/esha.json#/coils/24._inferred_type`: flipper
- `games/esha.json#/coils/24._note`: Framework constant sLLFlipper=48 from core.vbs/S11.VBS
- `games/esha.json#/lamps/0._vlm_array`: BL_IN_L1
- `games/esha.json#/lamps/0._note`: Also used as backglass lamp (Controller.Lamp(1) controls FlBGL1 visibility in VR mode)
- `games/esha.json#/lamps/1._vlm_array`: BL_IN_L2
- `games/esha.json#/lamps/1._note`: Also used as backglass lamp (Controller.Lamp(2) controls FlBGL2 visibility in VR mode)
- `games/esha.json#/lamps/2._vlm_array`: BL_IN_L3
- `games/esha.json#/lamps/2._note`: Also used as backglass lamp (Controller.Lamp(3) controls FlBGL3 visibility in VR mode)
- `games/esha.json#/lamps/3._vlm_array`: BL_IN_L4
- `games/esha.json#/lamps/3._note`: Also used as backglass lamp (Controller.Lamp(4) controls FlBGL4 visibility in VR mode)
- `games/esha.json#/lamps/4._vlm_array`: BL_IN_L5
- `games/esha.json#/lamps/4._note`: Also used as backglass lamp (Controller.Lamp(5) controls FlBGL5 visibility in VR mode)
- `games/esha.json#/lamps/5._vlm_array`: BL_IN_L6
- `games/esha.json#/lamps/5._note`: Also used as backglass lamp (Controller.Lamp(6) controls FlBGL6 visibility in VR mode)
- `games/esha.json#/lamps/6._vlm_array`: BL_IN_L7
- `games/esha.json#/lamps/7._vlm_array`: BL_IN_L8
- `games/esha.json#/lamps/8._vlm_array`: BL_IN_L9
- `games/esha.json#/lamps/9._vlm_array`: BL_IN_L10
- `games/esha.json#/lamps/10._vlm_array`: BL_IN_L11
- `games/esha.json#/lamps/11._vlm_array`: BL_IN_L12
- `games/esha.json#/lamps/12._vlm_array`: BL_IN_L13
- `games/esha.json#/lamps/13._vlm_array`: BL_IN_L14
- `games/esha.json#/lamps/14._vlm_array`: BL_IN_L15
- `games/esha.json#/lamps/15._vlm_array`: BL_IN_L16
- `games/esha.json#/lamps/16._vlm_array`: BL_IN_L17
- `games/esha.json#/lamps/16._note`: On Institute building — animates with building elevator via L17a_Animate
- `games/esha.json#/lamps/17._vlm_array`: BL_IN_L18
- `games/esha.json#/lamps/17._note`: On Institute building — animates with building elevator via L18a_Animate
- `games/esha.json#/lamps/18._vlm_array`: BL_IN_L19
- `games/esha.json#/lamps/18._note`: On Institute building — animates with building elevator via L19a_Animate
- `games/esha.json#/lamps/19._vlm_array`: BL_IN_L20
- `games/esha.json#/lamps/19._note`: On Institute building — animates with building elevator via L20a_Animate
- `games/esha.json#/lamps/20._vlm_array`: BL_IN_L21
- `games/esha.json#/lamps/21._vlm_array`: BL_IN_L22
- `games/esha.json#/lamps/22._vlm_array`: BL_IN_L23
- `games/esha.json#/lamps/23._vlm_array`: BL_IN_L24
- `games/esha.json#/lamps/24._vlm_array`: BL_IN_L25
- `games/esha.json#/lamps/25._vlm_array`: BL_IN_L26
- `games/esha.json#/lamps/25._note`: Located on stand-up target sw21 (BL_IN_L26 contains LM_IN_L26_sw21)
- `games/esha.json#/lamps/26._vlm_array`: BL_IN_L27
- `games/esha.json#/lamps/26._note`: Located on stand-up target sw22 (BL_IN_L27 contains LM_IN_L27_sw22)
- `games/esha.json#/lamps/27._vlm_array`: BL_IN_L28
- `games/esha.json#/lamps/28._vlm_array`: BL_IN_L29
- `games/esha.json#/lamps/29._vlm_array`: BL_IN_L30
- `games/esha.json#/lamps/30._vlm_array`: BL_IN_L31
- `games/esha.json#/lamps/31._vlm_array`: BL_IN_L32
- `games/esha.json#/lamps/32._vlm_array`: BL_IN_L33
- `games/esha.json#/lamps/33._vlm_array`: BL_IN_L34
- `games/esha.json#/lamps/34._vlm_array`: BL_IN_L35
- `games/esha.json#/lamps/35._vlm_array`: BL_IN_L36
- `games/esha.json#/lamps/36._vlm_array`: BL_IN_L37
- `games/esha.json#/lamps/37._vlm_array`: BL_IN_L38
- `games/esha.json#/lamps/38._vlm_array`: BL_IN_L39
- `games/esha.json#/lamps/39._vlm_array`: BL_IN_L40
- `games/esha.json#/lamps/40._vlm_array`: BL_IN_L41
- `games/esha.json#/lamps/41._vlm_array`: BL_IN_L42
- `games/esha.json#/lamps/42._vlm_array`: BL_IN_L43
- `games/esha.json#/lamps/43._vlm_array`: BL_IN_L44
- `games/esha.json#/lamps/44._vlm_array`: BL_IN_L45
- `games/esha.json#/lamps/45._vlm_array`: BL_IN_L46
- `games/esha.json#/lamps/46._vlm_array`: BL_IN_L47
- `games/esha.json#/lamps/47._vlm_array`: BL_IN_L48
- `games/esha.json#/lamps/48._vlm_array`: BL_IN_L49a
- `games/esha.json#/lamps/48._note`: VPX object suffix 'a' — mapped as L49a in VLM
- `games/esha.json#/lamps/49._vlm_array`: BL_IN_L50
- `games/esha.json#/lamps/49._note`: Located near stand-up target sw19 (BL_IN_L50 contains LM_IN_L50_sw19)
- `games/esha.json#/lamps/50._vlm_array`: BL_IN_L51
- `games/esha.json#/lamps/51._vlm_array`: BL_IN_L52
- `games/esha.json#/lamps/51._note`: Located near gate1 (BL_IN_L52 contains LM_IN_L52_gate1)
- `games/esha.json#/lamps/52._vlm_array`: BL_IN_L53
- `games/esha.json#/lamps/53._vlm_array`: BL_IN_L54
- `games/esha.json#/lamps/54._vlm_array`: BL_IN_L55
- `games/esha.json#/lamps/55._vlm_array`: BL_IN_L56
- `games/esha.json#/lamps/56._vlm_array`: BL_IN_L57a
- `games/esha.json#/lamps/56._note`: VPX object suffix 'a' — mapped as L57a in VLM
- `games/esha.json#/_source/confidence_notes`: High confidence on switches/coils. VPW table uses direct Controller.Switch() calls rather than named Const sw* constants — switch IDs inferred from VPX object names (sw10, sw11, etc.) and Controller.Switch() assignments. Lamps extracted from VLM BL_IN_L* arrays (VPW baked lighting system); lamp numbers are L1-L57 from the ROM lamp matrix. Flasher lamps mapped via SolModCallBack. Institute elevator uses switches 25/26 as position encoders (not simple open/close). sLRFlipper=46, sLLFlipper=48 are S11.VBS framework constants from core.vbs. Switch 42 is set by diverter animation timer, not a physical switch handler.

## Unresolved questions

- Is the I/O enumeration complete for every supported physical/controller variant?
- Which inferred VPX behaviors reflect real hardware, and which are table-script conveniences?
- Are all mechanism home states, sensors, motion constraints, and ball interactions documented?

## Sources

- `legacy.game.esha`: `games/esha.json` at the pinned migration revision.
