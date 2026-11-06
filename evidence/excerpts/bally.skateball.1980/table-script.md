# Skateball — exact retained table's controller contract

Source: `Skateball (Bally 1980) 1.0.4.vpx`, SHA-256 `ddbcae8cdc87ccdd7305f02ad853bd039d4b6489b25bcd2b82c0c8e03e07fb02`, extracted by vpxtool to `script.vbs`, SHA-256 `79336a53246582251087cd3a0892fe0e228737ea9e626813e2010bdcd65928c7`. Manually reviewed source-code transcription; statements summarize complete relevant handler regions, preserving public addresses. JPSalas is credited in the header, Bally 1980, four players. The table's runtime binding is evidence; its physics tuning and visual placement do not establish physical wiring.

The embedded script loads `Bally.vbs` 3.26, selects `cGameName = "skatebll"`, and sets `HandleKeyboard = 0`, `HandleMechanics = 0`. `vpmNudge.TiltSwitch = 7`.

| Region | Complete address contract |
|---|---|
| Table init: outhole | `bsTrough.InitNoTrough BallRelease, 8, 80, 6`; `Drain_Hit` calls `bsTrough.AddBall Me`; output 7 calls `bsTrough.SolOut` |
| Table init: saucer | `bsSaucer.InitSaucer sw5, 5, 195, 20`; force variance 2, angle variance 3; `sw5_Hit` adds the ball; output 2 calls `bsSaucer.SolOut` |
| SKATE bank | Objects/switches 24,23,22,21,20 in that order; the matching `_Dropped` handlers call positions 1,2,3,4,5; output 8 calls `dtbankL.SolDropUp` |
| Middle bank | Objects/switches 4,3,2; matching `_Dropped` handlers call positions 1,2,3; output 10 calls `dtbankM.SolDropUp` |
| Top bank | Objects/switches 28,27,26; matching `_Dropped` handlers call positions 1,2,3; output 9 calls `dtbankT.SolDropUp` |
| Scoring rubbers | All seven `sw17a_Hit` through `sw17g_Hit` pulse public 17 |
| Bumpers | `Bumper1_Hit` pulses 40; `Bumper2_Hit` pulses 38; `Bumper3_Hit` pulses 39 |
| Slingshots | Left sling pulses 37; right sling pulses 36 |
| Rollover hit/unhit handlers | Objects `sw13,sw14,sw15,sw18,sw19,sw30,sw31,sw34,sw35` set their matching public address to 1 on hit and 0 on unhit |
| Spinner | `sw33_Spin` pulses 33 |
| Right button | Right keydown sets matrix 32 true, right keyup sets it false; both also call Bally library key handling |
| Other explicit callbacks | Output 6 plays knocker sound; `SolCallback(25) = "vpmNudge.SolGameOn"` is unreachable on this BY35 driver |
| Flippers | `sLRFlipper` calls `SolRFlipper`, which moves both RightFlipper and RightFlipper1; `sLLFlipper` calls `SolLFlipper`, which moves both LeftFlipper and LeftFlipper1 |

The lower and upper coils are not assigned independent runtime callbacks. `Bally.vbs`/`core.vbs` determine the constants; the retained current library uses 46 and 48. The canonical definition describes physical paired flippers from factory wiring.

The lamp update idiom reads `Controller.ChangedLamps` into `LampState` and `FadingLevel`, then calls `UpdateLamps`. All 60 decoded addresses are consumed. There are 54 playfield addresses, driven by `NFadeL`/`NFadeLm` with additional `Flash` render helpers. Backbox 11, 13, 27, 29 and 61 call `NFadeT` with text messages and 45 calls `NFadeTm` for Game Over. Only nonexistent idle positions 16, 32 and 48 are commented in this region. `NFadeL 25, Bumper1L` (plus `NFadeLm 25, Bumper1La`) points at the left bumper and `NFadeL 57, Bumper2L` (plus `NFadeLm 57, Bumper2La`) at the right, opposite the factory bumper load names. That bumper swap is a confirmed defect in this table.

The rear-lane bindings pair switch 13 with lamp 24 (`NFadeLm 24, l24`) on the left and switch 15 with lamp 56 (`NFadeLm 56, l56`) on the right. `Light.l24` has center x 481.5 and `Light.l56` x 685.6491. The self-test and lamp wiring tables assign those pairs to lane #3 and lane #1 respectively without specifying sides. Figure V separately draws rollover circles 15, 14, 13 left-to-right, corroborating relative number order, but its differing upper-playfield geometry is not used as an absolute placement fit. The table's redrawn artwork and the physical replacement board in photo-026 label #1 left and #3 right. Thus both the switch and lamp layout differ from that replacement/artwork; original 1980 artwork orientation remains unverified. The definition retains crosswise switch anchors as observed placements and leaves lamps 24/56 unplaced. It does not describe the lane mismatch as a factory-proven defect. Insert lights are render proxies, not evidence of socket positions.

The pinned corpus's same-named script at revision `0c036bb61b4b4e8c778c37559f6795df8cd1521e` has SHA-256 `354b7dbcb62e4d5eff47d7d065257b340fabe397ce98e2e540461949cb952890`. It adds positional sound and changes `UseSolenoids` from 1 to 2 and saucer force from 20 to 17. The controller addresses and bank membership above agree. Its header says the sound edit was not verified; it is corroborating source only. The exact retained embedded script is the source used here.
