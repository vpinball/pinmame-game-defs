# NBA Fastbreak

Coverage: **partial - source-derived recreation knowledge requiring validation**

## Overview

Legacy evidence identifies this candidate as Bally (1997). The information below is preserved for recreation work but is not automatically treated as validated physical-machine fact.

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
- `games/nbaf.json#/switches/0._note`: sw1_Hit triggers BasketFlipper.RotateToStart
- `games/nbaf.json#/switches/1._note`: sw2_Hit triggers BasketFlipper.RotateToStart
- `games/nbaf.json#/switches/2._note`: sw3_Hit triggers BasketFlipper.RotateToStart
- `games/nbaf.json#/switches/3._note`: KeyDown/KeyUp PlungerKey sets Controller.Switch(11). Also plungerIM.Switch 15 references shooter lane.
- `games/nbaf.json#/switches/4._note`: Controller.Switch(12) via sw12_Hit/sw12_UnHit
- `games/nbaf.json#/switches/5._note`: vpmNudge.TiltSwitch = 14
- `games/nbaf.json#/switches/6._note`: plungerIM.Switch 15
- `games/nbaf.json#/switches/9._note`: vpmTimer.PulseSw 18
- `games/nbaf.json#/switches/10._note`: Controller.Switch(22) = 1 in init
- `games/nbaf.json#/switches/11._note`: vpmTimer.PulseSw 23 in Bumper2_Hit
- `games/nbaf.json#/switches/12._note`: Controller.Switch(24) = 1 in init
- `games/nbaf.json#/switches/13._note`: bsEject saucer — bsEject.AddBall 0 on hit
- `games/nbaf.json#/switches/16._note`: vpmTimer.PulseSw 28
- `games/nbaf.json#/switches/17._note`: bsTrough.InitSw 0,32,33,34,35,31,0,0 — position 5 is jam switch
- `games/nbaf.json#/switches/25._note`: vpmTimer.PulseSw 41
- `games/nbaf.json#/switches/26._note`: vpmTimer.PulseSw 42
- `games/nbaf.json#/switches/27._note`: vpmTimer.PulseSw 43
- `games/nbaf.json#/switches/30._note`: Also plays fx_metalrolling and sets ball velocity
- `games/nbaf.json#/switches/33._note`: Defender mech AddSw 51, 0, 1
- `games/nbaf.json#/switches/34._note`: Defender mech AddSw 52, 17, 18
- `games/nbaf.json#/switches/35._note`: Defender mech AddSw 53, 31, 32
- `games/nbaf.json#/switches/36._note`: Defender mech AddSw 54, 44, 45
- `games/nbaf.json#/switches/37._note`: Defender mech AddSw 55, 64, 65
- `games/nbaf.json#/switches/39._note`: vpmTimer.PulseSw 57 in LeftSlingShot_Slingshot
- `games/nbaf.json#/switches/40._note`: vpmTimer.PulseSw 58 in RightSlingShot_Slingshot
- `games/nbaf.json#/switches/41._note`: vpmTimer.PulseSw 61 in Bumper1_Hit
- `games/nbaf.json#/switches/42._note`: vpmTimer.PulseSw 62 in Bumper3_Hit
- `games/nbaf.json#/switches/45._note`: bsSaucer4 — InitSaucer sw65, 65
- `games/nbaf.json#/switches/46._note`: bsSaucer3 — InitSaucer sw66, 66
- `games/nbaf.json#/switches/47._note`: bsSaucer2 — InitSaucer sw67, 67
- `games/nbaf.json#/switches/48._note`: bsSaucer1 — InitSaucer sw68, 68
- `games/nbaf.json#/switches/49._note`: WPC flipper-coded switch. Controller.Switch(115).
- `games/nbaf.json#/switches/50._note`: WPC flipper-coded switch. Controller.Switch(117).
- `games/nbaf.json#/coils/0._vbscript_callback`: Auto_Plunger
- `games/nbaf.json#/coils/0._note`: Fires impulse plunger via PlungerIM.AutoFire
- `games/nbaf.json#/coils/1._note`: Commented out: 'SolCallBack(2) = Not Used'
- `games/nbaf.json#/coils/2._vbscript_callback`: SolDiverter2
- `games/nbaf.json#/coils/3._vbscript_callback`: vpmSolWall Diverter1,True,
- `games/nbaf.json#/coils/4._vbscript_callback`: bsEject.SolOut
- `games/nbaf.json#/coils/5._vbscript_callback`: RightGate.Open =
- `games/nbaf.json#/coils/6._vbscript_callback`: SolBasket
- `games/nbaf.json#/coils/6._note`: Controls backbox basketball mini-game flipper via BackBall kick
- `games/nbaf.json#/coils/7._note`: Handled via cvpmMagnet (MagnetCatch.Solenoid = 8), not SolCallback
- `games/nbaf.json#/coils/8._vbscript_callback`: bsTrough.SolOut
- `games/nbaf.json#/coils/9._note`: Commented out in VBS: 'SolCallBack(10) = vpmSolSound lSling'
- `games/nbaf.json#/coils/10._note`: Commented out in VBS: 'SolCallBack(11) = vpmSolSound lSling'
- `games/nbaf.json#/coils/11._note`: Commented out in VBS: 'SolCallBack(12) = vpmSolSound Jet1'
- `games/nbaf.json#/coils/12._note`: Commented out in VBS: 'SolCallBack(13) = vpmSolSound Jet1'
- `games/nbaf.json#/coils/13._note`: Commented out in VBS: 'SolCallBack(14) = vpmSolSound Jet1'
- `games/nbaf.json#/coils/14._vbscript_callback`: PassRight2
- `games/nbaf.json#/coils/14._note`: Alternate kick for bsSaucer2
- `games/nbaf.json#/coils/15._vbscript_callback`: PassLeft2
- `games/nbaf.json#/coils/15._note`: Alternate kick for bsSaucer2
- `games/nbaf.json#/coils/16._vbscript_callback`: FlashSol17
- `games/nbaf.json#/coils/16._note`: Comment: 'eject kickout flasher'
- `games/nbaf.json#/coils/17._vbscript_callback`: FlashSol18
- `games/nbaf.json#/coils/17._note`: Comment: 'left jet bumper'
- `games/nbaf.json#/coils/18._vbscript_callback`: FlashSol19
- `games/nbaf.json#/coils/18._note`: Comment: 'upper left / BG Left'
- `games/nbaf.json#/coils/19._vbscript_callback`: FlashSol20
- `games/nbaf.json#/coils/19._note`: Comment: 'upper right / BG Right'
- `games/nbaf.json#/coils/20._vbscript_callback`: SetLamp 122,
- `games/nbaf.json#/coils/20._note`: Comment: 'trophy insert TODO'
- `games/nbaf.json#/coils/21._vbscript_callback`: FlashSol24
- `games/nbaf.json#/coils/21._note`: Comment: 'lower right left'
- `games/nbaf.json#/coils/22._vbscript_callback`: PassRight1
- `games/nbaf.json#/coils/22._note`: Alternate kick for bsSaucer1
- `games/nbaf.json#/coils/23._vbscript_callback`: PassLeft3
- `games/nbaf.json#/coils/23._note`: Alternate kick for bsSaucer3
- `games/nbaf.json#/coils/24._vbscript_callback`: PassRight3
- `games/nbaf.json#/coils/24._note`: Alternate kick for bsSaucer3
- `games/nbaf.json#/coils/25._vbscript_callback`: PassLeft4
- `games/nbaf.json#/coils/25._note`: Alternate kick for bsSaucer4
- `games/nbaf.json#/coils/26._vbscript_callback`: bsSaucer1.SolOut
- `games/nbaf.json#/coils/27._vbscript_callback`: bsSaucer2.SolOut
- `games/nbaf.json#/coils/28._vbscript_callback`: bsSaucer3.SolOut
- `games/nbaf.json#/coils/29._vbscript_callback`: bsSaucer4.SolOut
- `games/nbaf.json#/coils/30._note`: Handled via cvpmMech (mDefender.Sol1 = 37), not SolCallback
- `games/nbaf.json#/coils/31._note`: Handled via cvpmMech (mDefender.Sol2 = 38), not SolCallback
- `games/nbaf.json#/coils/32._note`: Commented out in VBS: 'SolCallBack(39) = ClockEnable'
- `games/nbaf.json#/coils/33._note`: Commented out in VBS: 'SolCallBack(40) = ClockCount'
- `games/nbaf.json#/coils/34._vbscript_callback`: SolRFlipper
- `games/nbaf.json#/coils/34._note`: Framework alias sLRFlipper = 46 (from WPC.VBS/core.vbs)
- `games/nbaf.json#/coils/35._vbscript_callback`: SolLFlipper
- `games/nbaf.json#/coils/35._note`: Framework alias sLLFlipper = 48 (from WPC.VBS/core.vbs)
- `games/nbaf.json#/lamps/13._note`: Also mapped to l26a (dual VPX object)
- `games/nbaf.json#/lamps/22._note`: Also mapped to l37a (dual VPX object)
- `games/nbaf.json#/lamps/23._note`: Also mapped to l38a (dual VPX object)
- `games/nbaf.json#/lamps/26._note`: Also mapped to l43a (dual VPX object)
- `games/nbaf.json#/lamps/32._note`: Also mapped to l51a (dual VPX object)
- `games/nbaf.json#/lamps/34._note`: Also mapped to l53a (dual VPX object)
- `games/nbaf.json#/lamps/35._note`: Also mapped to l54a (dual VPX object)
- `games/nbaf.json#/lamps/36._note`: Also mapped to l55a (dual VPX object)
- `games/nbaf.json#/lamps/40._note`: Also mapped to l61b (dual VPX object, FadeDisableLightingM)
- `games/nbaf.json#/lamps/45._note`: Also mapped to l66a (dual VPX object)
- `games/nbaf.json#/lamps/46._note`: Has flasher behavior via FlashRondo (Objlevel 9)
- `games/nbaf.json#/lamps/47._note`: Has flasher behavior via FlashRondo (Objlevel 8)
- `games/nbaf.json#/lamps/50._note`: Also mapped to l73a (dual VPX object)
- `games/nbaf.json#/lamps/53._note`: Also mapped to l76a (dual VPX object)
- `games/nbaf.json#/lamps/54._note`: Has flasher behavior via FlashRondo (Objlevel 6)
- `games/nbaf.json#/lamps/55._note`: Has flasher behavior via FlashRondo (Objlevel 7)
- `games/nbaf.json#/lamps/58._note`: Also mapped to l83a (dual VPX object)
- `games/nbaf.json#/lamps/62._note`: Uses NFadeL (single object, no multi)
- `games/nbaf.json#/lamps/63._note`: Uses NFadeL (single object, no multi)
- `games/nbaf.json#/_source/confidence_notes`: Extracted directly from VPW VBS source. All switches from sw*_Hit/Controller.Switch() handlers. Coils from SolCallback assignments (active and commented). Lamps from UpdateLamps NfadeLm/NFadeL calls. Lamp descriptions are from VPX object names only — no PinMAME cross-referencing. Flashers 17-20,22,24 are solenoid-driven via FlashSol* subs. Lamps 67,68,77,78 have flasher behavior via FlashRondo. Defender mechanism (sol 37/38) and magnet (sol 8) handled via cvpmMech/cvpmMagnet, not SolCallback.

## Unresolved questions

- Is the I/O enumeration complete for every supported physical/controller variant?
- Which inferred VPX behaviors reflect real hardware, and which are table-script conveniences?
- Are all mechanism home states, sensors, motion constraints, and ball interactions documented?

## Sources

- `legacy.game.nbaf`: `games/nbaf.json` at the pinned migration revision.
