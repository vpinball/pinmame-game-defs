# Mary Shelley's Frankenstein table script bindings

Source: the retained table `Mary Shelley's Frankenstein (Sega 1995) v1.2.vpx` (SHA-256 `6f254182c77934f6a62fb02f675578532a40d14b87902a2944d1ba56280c3d2c`, table info "Schreibi34, Herweh", version 1.0.2), script extracted by vpxtool git:v0.33.3 as `script.vbs` (SHA-256 `53f8c80ad721dd92916c0d318decf95b4c4434c94a3c0efa3648b87f332fe571`). Machine-specific bindings, summarized factually with script line numbers.

## Library and controller (lines 158-232)

- `Const cGameName = "frankst"` (158); `LoadVPM "01550000", "DE.VBS", 3.26` (171); `.HandleMechanics = False`, `.HandleKeyboard = False` (190-191).
- `vpmNudge.TiltSwitch = 1` (212).
- Trough: `bsTrough` is a `cvpmBallStack` with `.InitSw 0, 14, 13, 12, 11, 10, 9, 0`, `.InitKick BallLockout, 80, 10`, `.Balls = 6` (217-222): six balls on 9-14 with the exit at 14, no table object per trough switch.

## Keys (lines 248-285)

- Plunger key writes 62 (`Controller.Switch(62)`) directly: the cabinet lever "The Switch".
- The flipper keys set local press flags; their direct writes to 63 and 64 are commented out (`' : Controller.Switch(63) = True`, `' : Controller.Switch(64) = True`), so only de.vbs `vpmKeyDown`/`vpmKeyUp` write the effective buttons 84 and 82.

## Solenoid callbacks (lines 293-320)

| Output | Callback | Script comment / effect |
| --- | --- | --- |
| 1 | SolLockout | `bsTrough.SolOut` from the trough to the BallLockout kicker |
| 2 | SolBallRelease | kicks `BallRelease` (switch 15) into the shooter lane |
| 3 | SolAutoLaunch | `vpmSolAutoPlungeS AutoPlunger` |
| 4 | SolLowerScoopEject | kicks the ball held at switch 32 |
| 5 | SolTopScoopEject | kicks the ball held at switch 31 |
| 6 | SolIceCaveEject | kicks the ball held at switch 55 and swings `pSaucer55Hammer` |
| 7 | SolVUKEject | kicks the ball held at switch 53 straight up |
| 8 | vpmSolSound Knocker | sound only |
| 9 | SolTrapLeftHand | opens `trUpperRampTrap1` (x 566), whose ball falls to `kFrankLeftHand`: the creature's left hand, on the player's right |
| 11 | SolGI | `SetGI Not IsOff`: the table's G.I. is lit while 11 is off |
| 12 | SolTrapRightHand | opens `trUpperRampTrap2` (x 273), whose ball falls to `kFrankRightHand`, on the player's left |
| 13 | SolFranksArms | swings both creature arms; at the top of the swing `ThrowBall` kicks each hand's ball and closes both trap doors |
| 14 | SolOrbitDiverter | makes the ramp `rDiverter` collidable while on |
| 16 | SolKickback | enables the `Kickback` kicker under the left outlane |
| 15, 25-31 | SolFlasher 0-7 | comments: 15 "around VUK", 25 "above ANK", 26 "above FR", 27 "above IN", 28 "at pop bumpers", 29 "at spinner", 30 "upper left corner", 31 "around VUK" |
| sLLFlipper, sLRFlipper | SolLFlipper, SolRFlipper | SolRFlipper moves both `RightFlipper` and `RightUpperFlipper` |

No callback is bound to 10 (the A/B relay) or 32.

## Switches

- Rollovers and gates 16, 33-40, 45, 46 and 56 are triggers named `sw<n>` that set and clear their switch; 54 is the spinner `sw54` (`vpmTimer.PulseSw 54` per spin).
- Stand-up targets 17-29 are hit targets `sw17`-`sw29` pulsed by `MoveStandUpTarget`.
- Bumpers `Bumper13`-`Bumper16` pulse 41-44; the slingshot walls pulse 47 and 48.
- Ball holders 31, 32, 53 and 55 are set by the table's ball-capture code (lines 1736-1770) and cleared by the kick routines.
- The script never writes 1-8 except through de.vbs (tilt 1, coin and start keys).

## Lamps (lines 1112-1146)

`InitLights InsertLights` maps every light of the InsertLights collection to the lamp number in its TimerInterval. The `LampTimer` routes lamps 13-16 to the bumper caps (`aBumperLight` lBumper13-16), 29 and 30 to `fPlasticBulb29`/`lPlasticBulb29` and `fPlasticBulb30`/`lPlasticBulb30`, 31 and 32 to `fPlasticBulb31`/`fPlasticBulb32` (sharing `lPlasticBulb30`), 48 to `lPlasticBulb48` and 56 to `lPlasticBulb56`; every other number goes to its InsertLights objects. The insert light `l40` carries TimerInterval 39, so the table lights it with lamp 39; lamp 40 drives only the reflection helper `l40a`.

## Table defects noted (not machine facts)

- `l40` bound to lamp 39 (above).
- The creature head is animated by the table's own timer modes (`AnimateFranksHead`), not from any PinMAME output.
