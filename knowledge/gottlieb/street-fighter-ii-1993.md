# Street Fighter II

Coverage: **partial - source-derived recreation knowledge requiring validation**

## Overview

Legacy evidence identifies this candidate as Gottlieb (1993). The information below is preserved for recreation work but is not automatically treated as validated physical-machine fact.

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

- `games/street-fighter-ii.json#/switches/0._vbscript_name`: swTournament
- `games/street-fighter-ii.json#/switches/0._note`: Const swTournament = 5. Controller.Switch(5) set on RightMagnaSave key.
- `games/street-fighter-ii.json#/switches/1._note`: vpmTimer.PulseSw 10. Bumper1_Hit fires PulseSw 10.
- `games/street-fighter-ii.json#/switches/2._note`: vpmTimer.PulseSw(11). Fired from LeftSlingShot_Slingshot event.
- `games/street-fighter-ii.json#/switches/3._note`: vpmTimer.PulseSw(12). Fired from RightSlingShot_Slingshot event.
- `games/street-fighter-ii.json#/switches/4._note`: Controller.Switch(13) on/off via sw13_Hit/UnHit. Kicked by SolOutSw13 (sol 10).
- `games/street-fighter-ii.json#/switches/5._note`: Controller.Switch(14) on/off via sw14_Hit/UnHit. Kicked by SolOutSw14 (sol 11).
- `games/street-fighter-ii.json#/switches/6._note`: vpmTimer.PulseSw 15. Fired in UpdateCar_Timer when car crunch collision occurs (deltay>0 and dCrunch<CrunchDist). Not a physical VPX switch.
- `games/street-fighter-ii.json#/switches/7._note`: Controller.Switch(21) = 1 in sw21_Hit. Trough eject sol 29 kicks from sw21. sw31b_UnHit clears Controller.Switch(21). This is the primary drain/outhole switch.
- `games/street-fighter-ii.json#/switches/8._note`: Controller.Switch(22) on/off. Checked in KeyUp to determine plunger release sound.
- `games/street-fighter-ii.json#/switches/9._note`: sw30_Hit fires vpmTimer.PulseSw 20 (NOT 30). Comment says 'Switches 20 and 30 need to be swapped. Need to confirm -FIXME'. Physical VPX target sw30 sends ROM switch 20.
- `games/street-fighter-ii.json#/switches/10._note`: sw20_Hit fires vpmTimer.PulseSw 30 (NOT 20). Comment says 'Switches 20 and 30 need to be swapped. Need to confirm -FIXME'. Physical VPX target sw20 sends ROM switch 30.
- `games/street-fighter-ii.json#/switches/11._note`: Controller.Switch(31) on/off via sw31a_Hit/UnHit. Part of custom 3-ball trough chain: sw31o -> sw31a -> sw31b -> sw21. sw31a is the middle trough position.
- `games/street-fighter-ii.json#/switches/12._note`: Controller.Switch(32) on/off via sw32_Hit/UnHit.
- `games/street-fighter-ii.json#/switches/13._note`: Controller.Switch(33) on/off. sw33_Hit also calls WireRampOff. Kicked by SolOutSw33 (sol 4) with kickz.
- `games/street-fighter-ii.json#/switches/14._note`: Controller.Switch(34) on/off. sw34_Hit also calls WireRampOff. Kicked by SolOutSw34 (sol 5) with kickz.
- `games/street-fighter-ii.json#/switches/15._note`: Controller.Switch(80) on/off. sw80_Hit calls WireRampOff then WireRampOn True (plastic ramp).
- `games/street-fighter-ii.json#/switches/16._note`: vpmTimer.PulseSw 81. Fired in UpdateCar_Timer when dCrunch >= CrunchDist (full car crush). Also triggers F01 flasher. Not a physical VPX switch.
- `games/street-fighter-ii.json#/switches/17._note`: Controller.Switch(82) set in KeyDown/KeyUp for LeftFlipperKey. GTS3 flipper button switch convention.
- `games/street-fighter-ii.json#/switches/18._note`: Controller.Switch(83) set in KeyDown/KeyUp for RightFlipperKey. GTS3 flipper button switch convention.
- `games/street-fighter-ii.json#/switches/19._note`: Controller.Switch(90) on/off. sw90_Hit calls WireRampOn True (plastic ramp).
- `games/street-fighter-ii.json#/switches/20._note`: Controller.Switch(91) on/off. sw91_Hit calls WireRampOn False (wire ramp).
- `games/street-fighter-ii.json#/switches/21._note`: STHit 92 — StandupTarget class with animated pushback. PulseSw 92 fired via STAnimate.
- `games/street-fighter-ii.json#/switches/22._note`: STHit 93 — StandupTarget class with animated pushback. PulseSw 93 fired via STAnimate.
- `games/street-fighter-ii.json#/switches/23._note`: STHit 94 — StandupTarget class with animated pushback. PulseSw 94 fired via STAnimate.
- `games/street-fighter-ii.json#/switches/24._note`: Controller.Switch(95) on/off via sw95_Hit/UnHit.
- `games/street-fighter-ii.json#/switches/25._note`: Controller.Switch(96) on/off via sw96_Hit/UnHit.
- `games/street-fighter-ii.json#/switches/26._note`: vpmTimer.PulseSw 100. Fired from sw100_Hit.
- `games/street-fighter-ii.json#/switches/27._note`: Controller.Switch(101) on/off. sw101_Hit calls WireRampOn False (wire ramp).
- `games/street-fighter-ii.json#/switches/28._note`: STHit 102 — StandupTarget class with animated pushback. PulseSw 102 fired via STAnimate.
- `games/street-fighter-ii.json#/switches/29._note`: STHit 103 — StandupTarget class with animated pushback. PulseSw 103 fired via STAnimate.
- `games/street-fighter-ii.json#/switches/30._note`: STHit 104 — StandupTarget class with animated pushback. PulseSw 104 fired via STAnimate.
- `games/street-fighter-ii.json#/switches/31._note`: Controller.Switch(105) on/off via sw105_Hit/UnHit.
- `games/street-fighter-ii.json#/switches/32._note`: Controller.Switch(106) on/off via sw106_Hit/UnHit.
- `games/street-fighter-ii.json#/switches/33._note`: Controller.Switch(110) on/off. sw110_UnHit calls WireRampOff.
- `games/street-fighter-ii.json#/switches/34._note`: Controller.Switch(111) on/off via sw111_Hit/UnHit.
- `games/street-fighter-ii.json#/switches/35._note`: STHit 112 — StandupTarget class with animated pushback. PulseSw 112 fired via STAnimate.
- `games/street-fighter-ii.json#/switches/36._note`: STHit 113 — StandupTarget class with animated pushback. PulseSw 113 fired via STAnimate.
- `games/street-fighter-ii.json#/switches/37._note`: Controller.Switch(114) on/off via sw114_Hit/UnHit.
- `games/street-fighter-ii.json#/switches/38._note`: Controller.Switch(115) on/off via sw115_Hit/UnHit.
- `games/street-fighter-ii.json#/switches/39._note`: Controller.Switch(116) on/off via sw116_Hit/UnHit.
- `games/street-fighter-ii.json#/switches/40._note`: vpmNudge.TiltSwitch = 151.
- `games/street-fighter-ii.json#/coils/0._inferred_type`: bumper
- `games/street-fighter-ii.json#/coils/0._vbscript_callback`: (commented out)
- `games/street-fighter-ii.json#/coils/0._note`: SolCallback(1) commented out with comment 'Pop bumper'. Handled by VPX physics.
- `games/street-fighter-ii.json#/coils/1._inferred_type`: slingshot
- `games/street-fighter-ii.json#/coils/1._vbscript_callback`: (commented out)
- `games/street-fighter-ii.json#/coils/1._note`: SolCallback(2) commented out with comment 'Left sling'. Handled by VPX physics.
- `games/street-fighter-ii.json#/coils/2._inferred_type`: slingshot
- `games/street-fighter-ii.json#/coils/2._vbscript_callback`: (commented out)
- `games/street-fighter-ii.json#/coils/2._note`: SolCallback(3) commented out with comment 'Right sling'. Handled by VPX physics.
- `games/street-fighter-ii.json#/coils/3._vbscript_callback`: SolOutSw33
- `games/street-fighter-ii.json#/coils/3._inferred_type`: ball_management
- `games/street-fighter-ii.json#/coils/3._note`: Kicks ball out of left scoop (sw33). sw33.kickz 0,40,90,30.
- `games/street-fighter-ii.json#/coils/4._vbscript_callback`: SolOutSw34
- `games/street-fighter-ii.json#/coils/4._inferred_type`: ball_management
- `games/street-fighter-ii.json#/coils/4._note`: Kicks ball out of right scoop (sw34). sw34.kickz 0,40,90,30.
- `games/street-fighter-ii.json#/coils/5._vbscript_callback`: SolDiv1
- `games/street-fighter-ii.json#/coils/5._inferred_type`: diverter
- `games/street-fighter-ii.json#/coils/5._note`: Controls Diverter1 drop state and Diverter1F rotation.
- `games/street-fighter-ii.json#/coils/6._vbscript_callback`: SolDiv2
- `games/street-fighter-ii.json#/coils/6._inferred_type`: diverter
- `games/street-fighter-ii.json#/coils/6._note`: Controls Diverter2 drop state and Diverter2F rotation.
- `games/street-fighter-ii.json#/coils/7._vbscript_callback`: SolDiv3
- `games/street-fighter-ii.json#/coils/7._inferred_type`: diverter
- `games/street-fighter-ii.json#/coils/7._note`: Controls LRampF rotation. Toggles LeftRampDown/LeftRampUp collidable state for ramp up/down position.
- `games/street-fighter-ii.json#/coils/8._vbscript_callback`: SolDiv4
- `games/street-fighter-ii.json#/coils/8._inferred_type`: diverter
- `games/street-fighter-ii.json#/coils/8._note`: Controls RRampF rotation. Toggles RightRampDown/RightRampUp collidable state for ramp up/down position.
- `games/street-fighter-ii.json#/coils/9._vbscript_callback`: SolOutSw13
- `games/street-fighter-ii.json#/coils/9._inferred_type`: ball_management
- `games/street-fighter-ii.json#/coils/9._note`: Kicks ball from sw13 kicker. sw13.kick 200,14.
- `games/street-fighter-ii.json#/coils/10._vbscript_callback`: SolOutSw14
- `games/street-fighter-ii.json#/coils/10._inferred_type`: ball_management
- `games/street-fighter-ii.json#/coils/10._note`: Kicks ball from sw14 kicker. sw14.kick 200,14.
- `games/street-fighter-ii.json#/coils/11._vbscript_callback`: CarReset
- `games/street-fighter-ii.json#/coils/11._inferred_type`: mechanism
- `games/street-fighter-ii.json#/coils/11._note`: Resets car crunch mechanism to home position. bCarReset = True triggers UpdateCarReset which moves CarP.y back at vy_reset velocity.
- `games/street-fighter-ii.json#/coils/12._vbscript_callback`: Flasher15
- `games/street-fighter-ii.json#/coils/12._inferred_type`: flasher
- `games/street-fighter-ii.json#/coils/12._note`: SolModCallBack(15). PWM flasher. AdjustBulbTint for incandescent simulation.
- `games/street-fighter-ii.json#/coils/13._vbscript_callback`: Flasher16
- `games/street-fighter-ii.json#/coils/13._inferred_type`: flasher
- `games/street-fighter-ii.json#/coils/13._note`: SolModCallBack(16). PWM flasher. AdjustBulbTint for incandescent simulation.
- `games/street-fighter-ii.json#/coils/14._vbscript_callback`: Flasher17
- `games/street-fighter-ii.json#/coils/14._inferred_type`: flasher
- `games/street-fighter-ii.json#/coils/14._note`: SolModCallBack(17). PWM flasher. AdjustBulbTint for incandescent simulation.
- `games/street-fighter-ii.json#/coils/15._vbscript_callback`: Flasher18
- `games/street-fighter-ii.json#/coils/15._inferred_type`: flasher
- `games/street-fighter-ii.json#/coils/15._note`: SolModCallBack(18). PWM flasher. AdjustBulbTint for incandescent simulation.
- `games/street-fighter-ii.json#/coils/16._vbscript_callback`: Flasher19
- `games/street-fighter-ii.json#/coils/16._inferred_type`: flasher
- `games/street-fighter-ii.json#/coils/16._note`: SolModCallBack(19). PWM flasher. AdjustBulbTint for incandescent simulation.
- `games/street-fighter-ii.json#/coils/17._vbscript_callback`: Flasher20
- `games/street-fighter-ii.json#/coils/17._inferred_type`: flasher
- `games/street-fighter-ii.json#/coils/17._note`: SolModCallBack(20). PWM flasher. AdjustBulbTint for incandescent simulation.
- `games/street-fighter-ii.json#/coils/18._vbscript_callback`: Flasher21
- `games/street-fighter-ii.json#/coils/18._inferred_type`: flasher
- `games/street-fighter-ii.json#/coils/18._note`: SolModCallBack(21). PWM flasher. AdjustBulbTint for incandescent simulation.
- `games/street-fighter-ii.json#/coils/19._vbscript_callback`: Flasher22
- `games/street-fighter-ii.json#/coils/19._inferred_type`: flasher
- `games/street-fighter-ii.json#/coils/19._note`: SolModCallBack(22). PWM flasher. AdjustBulbTint for incandescent simulation.
- `games/street-fighter-ii.json#/coils/20._vbscript_callback`: Flasher23
- `games/street-fighter-ii.json#/coils/20._inferred_type`: flasher
- `games/street-fighter-ii.json#/coils/20._note`: SolModCallBack(23). PWM flasher. AdjustBulbTint for incandescent simulation.
- `games/street-fighter-ii.json#/coils/21._vbscript_callback`: SolRFlipper1
- `games/street-fighter-ii.json#/coils/21._inferred_type`: flipper
- `games/street-fighter-ii.json#/coils/21._note`: SolCallback(24). Comment: 'this is the underplayfield flipper'. Controls RightFlipper1 rotation and UpdateCar timer. Sets LowerFlipper flag.
- `games/street-fighter-ii.json#/coils/22._vbscript_callback`: SolSpinChunli
- `games/street-fighter-ii.json#/coils/22._inferred_type`: mechanism
- `games/street-fighter-ii.json#/coils/22._note`: Drives the spinning Chunli flipper animation. SpinningFlipper.startangle rotated at 0.64 rate. 4-frame visual animation (SpinFlip1-4). Motor sound plays while enabled.
- `games/street-fighter-ii.json#/coils/23._vbscript_callback`: SolBG
- `games/street-fighter-ii.json#/coils/23._inferred_type`: mechanism
- `games/street-fighter-ii.json#/coils/23._note`: Controls backglass GI. INVERTED: SolBG(False) = gibg.state=1 (ON). Separate from playfield GI (sol 31).
- `games/street-fighter-ii.json#/coils/24._vbscript_callback`: vpmSolSound "SolOn",
- `games/street-fighter-ii.json#/coils/24._inferred_type`: sound
- `games/street-fighter-ii.json#/coils/24._note`: VPM sound solenoid. Plays SolOn sound effect.
- `games/street-fighter-ii.json#/coils/25._vbscript_callback`: SolRelease
- `games/street-fighter-ii.json#/coils/25._inferred_type`: ball_management
- `games/street-fighter-ii.json#/coils/25._note`: Kicks ball from sw31o (deepest trough position) to shooter lane. sw31o.kick 57,10.
- `games/street-fighter-ii.json#/coils/26._vbscript_callback`: SolTrough
- `games/street-fighter-ii.json#/coils/26._inferred_type`: ball_management
- `games/street-fighter-ii.json#/coils/26._note`: Kicks ball from sw21 (drain/outhole) into trough. sw21.kick 57,20.
- `games/street-fighter-ii.json#/coils/27._vbscript_callback`: Knocker
- `games/street-fighter-ii.json#/coils/27._inferred_type`: knocker
- `games/street-fighter-ii.json#/coils/27._note`: Cabinet knocker solenoid. Calls KnockerSolenoid sub.
- `games/street-fighter-ii.json#/coils/28._vbscript_callback`: GIState
- `games/street-fighter-ii.json#/coils/28._inferred_type`: mechanism
- `games/street-fighter-ii.json#/coils/28._note`: Playfield GI relay. INVERTED: GIState(False) = GI ON (gilvl=1). GIState(True) = GI OFF (gilvl=0). Controls all lights in GI array.
- `games/street-fighter-ii.json#/coils/29._vbscript_callback`: (commented out)
- `games/street-fighter-ii.json#/coils/29._inferred_type`: mechanism
- `games/street-fighter-ii.json#/coils/29._note`: SolCallback(32) = 'GameOn' is commented out. Likely game-on relay but not implemented in VBS.
- `games/street-fighter-ii.json#/lamps/0._note`: LM_I_L0 lightmap. Illuminates LFlip/RFlip area. UseLamps=1 (VPX built-in handling).
- `games/street-fighter-ii.json#/lamps/1._note`: LM_CC_L02 lightmap. Car Crunch lamp 1 of 6. Illuminates car, lower playfield, layers.
- `games/street-fighter-ii.json#/lamps/2._note`: LM_CC_L03 lightmap. Car Crunch lamp 2 of 6.
- `games/street-fighter-ii.json#/lamps/3._note`: LM_CC_L04 lightmap. Car Crunch lamp 3 of 6.
- `games/street-fighter-ii.json#/lamps/4._note`: LM_CC_L05 lightmap. Car Crunch lamp 4 of 6.
- `games/street-fighter-ii.json#/lamps/5._note`: LM_CC_L06 lightmap. Car Crunch lamp 5 of 6.
- `games/street-fighter-ii.json#/lamps/6._note`: LM_CC_L07 lightmap. Car Crunch lamp 6 of 6.
- `games/street-fighter-ii.json#/lamps/7._note`: LM_I_L10 lightmap. Also has l10_sw95 association in VLM.
- `games/street-fighter-ii.json#/lamps/8._note`: LM_I_L11 lightmap. Illuminates LSling and sw105 area.
- `games/street-fighter-ii.json#/lamps/9._note`: LM_I_L12 lightmap. Illuminates RSling and sw106 area.
- `games/street-fighter-ii.json#/lamps/10._note`: LM_I_L13 lightmap. Also has sw96 association in VLM.
- `games/street-fighter-ii.json#/lamps/11._note`: LM_I_L14 lightmap. Illuminates LFlip/RFlip area.
- `games/street-fighter-ii.json#/lamps/12._note`: LM_I_L15 lightmap. Illuminates LSling area.
- `games/street-fighter-ii.json#/lamps/13._note`: LM_I_L16 lightmap.
- `games/street-fighter-ii.json#/lamps/14._note`: LM_I_L17 lightmap. Has l17a_animate for white insert brightness trick.
- `games/street-fighter-ii.json#/lamps/15._note`: LM_I_L20 lightmap. Illuminates RSling and Sling2 area.
- `games/street-fighter-ii.json#/lamps/16._note`: LM_I_L21 lightmap. Illuminates RSling area.
- `games/street-fighter-ii.json#/lamps/17._note`: LM_I_L22 lightmap. Has l22a_animate for white insert brightness trick.
- `games/street-fighter-ii.json#/lamps/18._note`: LM_I_L23 lightmap. Has l23a_animate for white insert brightness trick.
- `games/street-fighter-ii.json#/lamps/19._note`: LM_I_L24 lightmap.
- `games/street-fighter-ii.json#/lamps/20._note`: LM_I_L25 lightmap.
- `games/street-fighter-ii.json#/lamps/21._note`: LM_I_L26 lightmap. Has l26a_animate for white insert brightness trick.
- `games/street-fighter-ii.json#/lamps/22._note`: LM_I_L27 lightmap. Also illuminates RRampArm.
- `games/street-fighter-ii.json#/lamps/23._note`: LM_I_L30 lightmap. Illuminates LPF, sw104, sw94 area.
- `games/street-fighter-ii.json#/lamps/24._note`: LM_I_L31 lightmap. Illuminates Car, LPF, sw104 area.
- `games/street-fighter-ii.json#/lamps/25._note`: LM_I_L32 lightmap.
- `games/street-fighter-ii.json#/lamps/26._note`: LM_I_L33 lightmap. Illuminates sw103 and sw113 standup target area.
- `games/street-fighter-ii.json#/lamps/27._note`: LM_I_L34 lightmap. Has l34a_animate for white insert brightness trick. Illuminates sw103 and sw113 area.
- `games/street-fighter-ii.json#/lamps/28._note`: LM_I_L35 lightmap. Illuminates Bumper1Ring, sw103, sw112, sw113, sw30 area.
- `games/street-fighter-ii.json#/lamps/29._note`: LM_I_L36 lightmap. Illuminates Bumper1Ring, sw102, sw112, sw92 area.
- `games/street-fighter-ii.json#/lamps/30._note`: LM_I_L37 lightmap. Has l37a_animate for white insert brightness trick. Illuminates Bumper1Ring, sw112, sw92 area.
- `games/street-fighter-ii.json#/lamps/31._note`: LM_I_L40 lightmap. Illuminates upper left flipper area (LFlip1U).
- `games/street-fighter-ii.json#/lamps/32._note`: LM_I_L41 lightmap. Illuminates left ramp arm and ramp area.
- `games/street-fighter-ii.json#/lamps/33._note`: LM_I_L42 lightmap. Has l42a_animate. Illuminates left ramp arm, ramp, and Layer3.
- `games/street-fighter-ii.json#/lamps/34._note`: LM_I_L43 lightmap. Illuminates left ramp, sw103, sw93 area.
- `games/street-fighter-ii.json#/lamps/35._note`: LM_I_L44 lightmap. Illuminates left ramp, sw92, sw93 area.
- `games/street-fighter-ii.json#/lamps/36._note`: LM_I_L45 lightmap. Has l45a_animate. Illuminates Bumper1Ring and sw92 area.
- `games/street-fighter-ii.json#/lamps/37._note`: LM_I_L46 lightmap. Illuminates Car, LPF, sw103, sw113, sw93 area.
- `games/street-fighter-ii.json#/lamps/38._note`: LM_I_L47 lightmap. Has l47a_animate. Illuminates Layer3, sw103, sw113.
- `games/street-fighter-ii.json#/lamps/39._note`: LM_I_L50 lightmap. Illuminates upper left flipper area (LFlip1U).
- `games/street-fighter-ii.json#/lamps/40._note`: LM_I_L51 lightmap. Illuminates upper left flipper area (LFlip1U).
- `games/street-fighter-ii.json#/lamps/41._note`: LM_I_L52 lightmap. Has l52a_animate. Illuminates upper left flipper area (LFlip1U).
- `games/street-fighter-ii.json#/lamps/42._note`: LM_I_L53 lightmap. Has l53a_animate. Illuminates left ramp arm upper and ramp area.
- `games/street-fighter-ii.json#/lamps/43._note`: LM_I_L54 lightmap. Illuminates sw102 and sw92 area.
- `games/street-fighter-ii.json#/lamps/44._note`: LM_I_L55 lightmap. Illuminates sw102, sw112, sw92 area.
- `games/street-fighter-ii.json#/lamps/45._note`: LM_I_L56 lightmap. Illuminates sw102, sw112, sw92 area.
- `games/street-fighter-ii.json#/lamps/46._note`: LM_F_L57 lightmap. Flasher-style lamp. Illuminates Bumper1Ring, SpinFlip1/4, sw102, sw103, sw112, sw113, sw92, sw93 area.
- `games/street-fighter-ii.json#/lamps/47._note`: LM_I_L60 lightmap. Illuminates Car, LPF, Layer1/2, RFlip1 area.
- `games/street-fighter-ii.json#/lamps/48._note`: LM_A_L61 lightmap. Parts only. Topper/alphanumeric display backlight.
- `games/street-fighter-ii.json#/lamps/49._note`: LM_A_L62 lightmap. Parts only.
- `games/street-fighter-ii.json#/lamps/50._note`: LM_A_L63 lightmap. Parts only.
- `games/street-fighter-ii.json#/lamps/51._note`: LM_A_L64 lightmap. Parts only.
- `games/street-fighter-ii.json#/lamps/52._note`: LM_A_L65 lightmap. Parts only.
- `games/street-fighter-ii.json#/lamps/53._note`: LM_A_L66 lightmap. Parts only.
- `games/street-fighter-ii.json#/lamps/54._note`: LM_A_L67 lightmap. Parts only.
- `games/street-fighter-ii.json#/_source/confidence_notes`: High confidence extraction from VPW VBScript by Apophis/Gedankekojote97/Sixtoe. Platform detected as Gottlieb System 3 from LoadVPM call: LoadVPM '03060000', 'gts3.VBS', 3.10. ROM name 'sfight2' from Const cGameName. Trough is a custom non-framework design: 3 balls initialized in kickers sw31o, sw31a, sw31b. sw31a maps to Controller.Switch(31), sw31b triggers Controller.Switch(21). Trough eject (sol 29) kicks from sw21, ball release (sol 28) kicks from sw31o. UpdateTrough cascades balls through the three kickers. No cvpmTrough framework used. Car Crunch mechanism uses a captive ball (CarBall) with physics simulation — sol 14 resets car position, sw15 fires on crunch hits, sw81 fires on full crunch completion. Chunli spinning flipper (sol 25) rotates a visual flipper with 4-frame animation. Flipper button switches sw82/sw83 are set directly in KeyDown/KeyUp handlers for left/right flipper buttons (GTS3 convention). Standup targets use VPW StandupTarget class with PulseSw in STAnimate function. Switches 20 and 30 are swapped in VBS code (FIXME comment in script — sw20_Hit fires PulseSw 30 and vice versa). Lamps identified from VLM lightmap arrays: L0, L10-L17, L20-L27, L30-L37, L40-L47, L50-L56, L57 (flasher-lamp), L60, L61-L67 (alphanumeric/topper). Car crunch lamps L02-L07 are CC (car crunch) lamps. GI is inverted — GIState(False) turns GI ON (gilvl=1). Sol 26 controls backglass GI relay. Flashers 15-23 use SolModCallback (PWM). Sol 24 is the car/underplayfield flipper (RightFlipper1). Sol 27 is a sound solenoid (vpmSolSound). Commented-out solenoids: 1 (pop bumper), 2 (left sling), 3 (right sling) — handled by VPX physics. Sol 12, 13 not used. Sol 32 (GameOn) commented out.

## Unresolved questions

- Is the I/O enumeration complete for every supported physical/controller variant?
- Which inferred VPX behaviors reflect real hardware, and which are table-script conveniences?
- Are all mechanism home states, sensors, motion constraints, and ball interactions documented?

## Sources

- `legacy.game.street-fighter-ii`: `games/street-fighter-ii.json` at the pinned migration revision.
