# Data East Secret Service (1988)

## Identity and controller

Pinned PinMAME groups four 03/88 drivers under root `ssvc_a26`: root 2.6, `ssvc_b26` 2.6 alternate sound, `ssvc_e40` 4.0 Europe, and `ssvc_a42` 4.2 alternate sound. All use `INITGAMES11(ssvc, GEN_DE, de_dispAlpha2, FLIP3031, SNDBRD_DE1S, 0, 0)`. `GEN_DE` is generation `0x1000` in the shared System 11 core family, so the existing `pinmame.system-11` profile is reused unchanged.

`de_dispAlpha2` has exactly four entries: two seven-character 16-segment player rows beginning at segment 1 and 9, followed by two seven-character numeric rows beginning at 21 and 29. Unlike Data East's Alpha1 layout, it contains no credit/match or ball-in-play display entries. The definition therefore enumerates four displays and gives each a controlled cabinet/backbox `not_applicable` spatial record.

## Address model

The definition enumerates every switch and lamp address 1-64, Data East service switches -7/-6, Jumper W7 at DIP address 0, and all public solenoids 1-50 exposed when `custSol=0`. Switches 30 and 31 are printed as Left and Right Flipper EOS contacts. PinMAME's `FLIP3031` feeds player-button state into those EOS-numbered addresses; the preliminary cabinet schematic independently shows separate high-current flipper-button circuits, so the controller-facing and physical meanings remain a first-class conflict.

The production manual numbers eight shared-transistor pairs as 01L-08L and 01R-08R around the Left/Right relay at output 10. The operator numbering plus retained runtime place L flashers at public 1-8 and R mechanisms at public 25-32. Pinned `s11.c`, however, types only output 9 and muxed public 25-32 as #89 bulbs, GI at 11, and K1 at 10. That typing disagreement is preserved rather than choosing a silent correction.

## Ball handling and moving assemblies

The retained script supplies real causal topology. A three-ball trough occupies switches 47-49 and ejects through output 32; switch 46/output 26 is the outhole feeder. Switch 19/output 27 is the top-right eject. Switches 36-40 form a five-drop bank reset by output 28. The KGB Hideout captures at switch 11, reports the down position on 12, lowers on output 25, raises/ejects on output 30, and starts with switch 12 active. The White House lock stages balls at switches 41/42 and exits through output 16. Output 14 raises the center post, clears normally active switch 52, and a table timer lowers it again. Output 15 drives the left-outlane kickback at switch 32.

The production parts page identifies Ramp Assembly 515-5068-00, Russian Embassy Assembly 515-5073-00, Flipper Assembly 515-5038-00, Kick Back Assembly 500-5000-00, White House Assembly 515-5072-00, and both spinner assemblies. Three physical flippers are printed: lower left, lower right and upper right. The retained right callback moves both right flippers together; no separate upper-right EOS address is printed.

Pop bumpers and slingshots remain deliberately conservative. Production maps SP1-SP5 to red/clear/blue pop bumpers and left/right slingshots, and the preliminary schematic draws their switch-triggered circuits. But the retained script has no `SolCallback` for outputs 17-21. Sensor mechanisms are retained with empty actuator lists rather than converting printed labels or proximity into runtime topology.

## Lamp and spatial evidence

The retained header is `UseSolenoids=2, UseLamps=0, UseGI=0`. It contains neither `Lampz.MassAssign` nor `vpmMapLights`; instead `LampTimer` consumes `Controller.ChangedLamps` and `UpdateLamps` calls `NFadeL`/`NFadeLm`. Exactly 64 Light objects are named `L1` through `L64`. Those names support candidate visual coordinates only, not observed physical ROM-to-socket bindings. L22a and L39a/L39b are additional render emitters, not extra addresses.

Active `SolCallback(1)` through `(9)` route to pseudo-lamps 101-109. UpdateLamps exposes multiple visual emitters for 103 and 108, no visual object for 107, and several helper pairs for the others. Whole-line-commented callbacks 12 and 13 are stripped before attribution; they supply no coordinate. The nine extracted Flasher gameitems are ball-shadow/general render effects and are not treated as controller-output emitters. Exact bounds are 0,0 to 952,2162 and normalized as x/952, y/2162.

## Manual conflicts and limits

Both retained manuals have zero extractable characters. Production PDF pages 20-25 were freshly rendered at 400 dpi and read cell-by-cell; page 28 supplied construction parts. The preliminary schematics on PDF pages 11-14 are used only where they are the sole source, and production governs disagreements. The preliminary scan omits its printed page 20.

The production switch matrix says `10 Point` at 18, 27 and 45 while the following list says `310 Point`. Its lamp matrix and playfield-lamp list disagree at many addresses, including 5, 14-18 and 39-48; both complete readings are committed. The preliminary schematic calls SP2 Yellow Pop Bumper while production says Clear. The production coil table literally prints `BIU-YEL` for the right-flipper power lead while preliminary prints `BLU-YEL`. Production Coil Test also adds `Clear Mars` to output 13 where the detailed production table does not. Every disagreement remains a conflict with source-specific wording.

## Failure modes and what would complete the record

Likely service checks follow the proven topology: balls can jam across the three trough positions, the two White House lock positions, top-right eject, and KGB eater; the five-bank must return all targets; the up-post timer must restore its down switch; and the relay/coil compounds for kickback and Kickbig each include a 24 V relay plus 24-900 coil. Exact pulse widths, post dwell on hardware, public special-solenoid callbacks, and flipper/EOS polarity were not captured and must not be invented.

Completion needs a PinMAME/controller trace across both L/R relay states, runtime observation of outputs 17-21 while their switches fire, bench capture of button/EOS and three-flipper behavior, and a socket-address survey of the original playfield/back panel including GI. Until then the record remains partial.
