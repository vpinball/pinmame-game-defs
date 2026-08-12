# Data East Secret Service (1988)

## Identity and controller

Pinned PinMAME groups four 03/88 drivers under root `ssvc_a26`: root 2.6, `ssvc_b26` 2.6 alternate sound, `ssvc_e40` 4.0 Europe, and `ssvc_a42` 4.2 alternate sound. All use `INITGAMES11(ssvc, GEN_DE, de_dispAlpha2, FLIP3031, SNDBRD_DE1S, 0, 0)`. `GEN_DE` is Data East generation `0x1000`, not Williams System 11 hardware. The definition now reuses the reviewed `pinmame.dataeast` profile and no longer carries a controller-platform blocker.

The machine-level `inversion_applied_by_emulator` flag is true because consumers receive normalized public LibPinMAME states and must not invert them again. Independently, `INITGAMES11` aggregate-initializes the per-game `wpc.invSw` mask with zeroes and pinned `core.c` copies that exact mask to the runtime switch matrix. Neither fact settles physical EOS polarity or the unresolved three-flipper behavior.

`de_dispAlpha2` has exactly four entries: two seven-character 16-segment player rows beginning at segment 1 and 9, followed by two seven-character numeric rows beginning at 21 and 29. Unlike Data East's Alpha1 layout, it contains no credit/match or ball-in-play display entries. The definition therefore enumerates four displays and gives each a controlled cabinet/backbox `not_applicable` spatial record.

## Address model

The definition enumerates every switch and lamp address 1-64, Data East service switches -7/-6, Jumper W7 at DIP address 0, and all public solenoids 1-50 exposed when `custSol=0`. Switches 30 and 31 are printed as Left and Right Flipper EOS contacts. PinMAME's `FLIP3031` feeds player-button state into those EOS-numbered addresses; the production cabinet schematic independently shows separate high-current flipper-button circuits, so the controller-facing and physical meanings remain a first-class conflict.

The production manual numbers eight shared-transistor pairs as 01L-08L and 01R-08R around the Left/Right relay at output 10. The operator numbering plus retained runtime place L flashers at public 1-8 and R mechanisms at public 25-32. Pinned `s11.c`, however, types only output 9 and muxed public 25-32 as #89 bulbs, GI at 11, and K1 at 10. That typing disagreement is preserved rather than choosing a silent correction.

## Ball handling and moving assemblies

The retained script supplies real causal topology. A three-ball trough occupies switches 47-49 and ejects through output 32; switch 46/output 26 is the outhole feeder. Switch 19/output 27 is the top-right eject. Switches 36-40 form a five-drop bank reset by output 28. The KGB Hideout captures at switch 11, reports the down position on 12, lowers on output 25, raises/ejects on output 30, and starts with switch 12 active. The White House lock stages balls at switches 41/42 and exits through output 16. Output 14 raises the center post, clears normally active switch 52, and a table timer lowers it again. Output 15 drives the left-outlane kickback at switch 32.

The production parts page identifies Ramp Assembly 515-5068-00, Russian Embassy Assembly 515-5073-00, Flipper Assembly 515-5038-00, Kick Back Assembly 500-5000-00, White House Assembly 515-5072-00, and both spinner assemblies. Three physical flippers are printed: lower left, lower right and upper right. The retained right callback moves both right flippers together; no separate upper-right EOS address is printed.

Production maps SP1-SP5 to red/clear/blue pop bumpers and left/right slingshots, with SP6 unfitted, and the Coil Test explicitly numbers SP1-SP6 as public 17-22. The structured mechanisms therefore bind red pop 17, clear pop 18, blue pop 19, left sling 20, and right sling 21; public 22 is the unfitted SP6 physical driver. Pinned `s11.c` PIA comments plus `setSSSol`'s Data East offsets can be read as a conflicting SP1, SP3, SP4, SP6, SP5, SP2 public order, so all six mappings remain conflicted pending a LibPinMAME trace. The retained script has no `SolCallback` for these switch-triggered outputs, leaving pulse timing and actuator placement unresolved too.

This is an explicit exception to the repository runbook's former unconditional Data East permutation rule and to the working source-derived contracts in the merged Playboy, Time Machine, and Torpedo Alley definitions. Those siblings do not carry Secret Service's game-specific Coil Test pairing each public number with an SP identity. The runbook now conditions the source-derived rule on the available primary evidence; it does not resolve the cross-game disagreement, and a LibPinMAME trace remains mandatory.

The Coil Identification Table prints SP1/SP3/SP4 at Q8/Q10/Q11, while both production schematic views assign those circuits to Q11/Q8/Q10. Structured `wiring.driver_transistor` values follow the agreeing schematics; the literal table cells remain in the coil excerpt and each affected output note.

## Lamp and spatial evidence

The retained header is `UseSolenoids=2, UseLamps=0, UseGI=0`. It contains neither `Lampz.MassAssign` nor `vpmMapLights`; instead `LampTimer` consumes `Controller.ChangedLamps` and `UpdateLamps` calls `NFadeL`/`NFadeLm`. Exactly 64 Light objects are named `L1` through `L64`. Those names support candidate visual coordinates only, not observed physical ROM-to-socket bindings. L22a and L39a/L39b are additional render emitters, not extra addresses.

Active `SolCallback(1)` through `(9)` route to pseudo-lamps 101-109. UpdateLamps exposes multiple visual emitters for 103 and 108, no visual object for 107, and several helper pairs for the others. Whole-line-commented callbacks 12 and 13 are stripped before attribution; they supply no coordinate. The nine extracted Flasher gameitems are ball-shadow/general render effects and are not treated as controller-output emitters. Exact bounds are 0,0 to 952,2162 and normalized as x/952, y/2162.

Outputs 6 and 7 print a White House or Russian Embassy playfield feature plus a backglass emitter, and output 9 prints KGB Hideout plus Music Credits on the speaker panel. The retained table supplies at most one visual proxy for each mixed-location pair and none for 7, so all three omit `spatial` rather than turning missing table objects into a cabinet-only verdict. Output 13 also omits `spatial`: its detailed row says Secret Service (Backglass), but the conflicting Coil Test adds Clear Mars, whose physical plane and socket are unresolved.

## Manual conflicts and limits

The retained production manual has zero extractable characters. PDF pages 20-25 were freshly rendered at 400 dpi and read cell-by-cell; page 28 supplied construction parts. Schematic pages 30 and 32-34 were rendered at 300 dpi and visually checked for cabinet controls, switch and lamp matrices, driver routing, special coils, and flipper wiring.

The production switch matrix and following list differ at addresses 3, 11-13, 18, 25, 27-32, 41-45; this includes the material `Left Kickback`/`Laser Kickback` disagreement at 32, not just the `10 Point`/`310 Point` rows. Its lamp matrix and playfield-lamp list disagree at many addresses, including 5, 14-18 and 39-48; both complete readings are committed. The production Coil Identification Table literally prints `BIU-YEL` for the right-flipper power lead while the production wiring diagram labels CN3 pin 6 `BLU-YEL`. Production Coil Test also adds `Clear Mars` to output 13 where the detailed production table does not. Every disagreement remains a conflict with source-specific wording.

## Failure modes and what would complete the record

Likely service checks follow the proven topology: balls can jam across the three trough positions, the two White House lock positions, top-right eject, and KGB eater; the five-bank must return all targets; the up-post timer must restore its down switch; and the relay/coil compounds for kickback and Kickbig each include a 24 V relay plus 24-900 coil. Exact pulse widths, post dwell on hardware, special-solenoid public callbacks/timing, and flipper/EOS polarity were not captured and must not be invented.

Completion needs a PinMAME/controller trace across both L/R relay states, public-output and pulse-timing observation of outputs 17-22 while their switches fire, bench capture of button/EOS and three-flipper behavior, and a socket-address survey of the original playfield/back panel including GI. Until then the record remains partial.
