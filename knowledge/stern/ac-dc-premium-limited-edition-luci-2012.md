# AC/DC Premium / Limited Edition / LUCI Premium recreation knowledge

## Identity and variants

This definition covers every in-scope h and hc PinMAME driver from 1.50 through 1.70 for the shared Stern Premium, Limited Edition, and LUCI Premium physical playfield. LUCI changes art and presentation; the LE trim packages and colored-ROM derivatives do not change controller-facing devices or mechanisms.

## Source precedence

The known-working VPW-derived LUCI 1.1.4 script is ground truth for public PinMAME addresses, callback routing, initial ball state, and mechanism causality. The exact Premium and LUCI manuals are authoritative for construction, wiring, assemblies, connector identities, and parts. Pinned PinMAME source defines the SAM transport, clone lineage, auxiliary-board translation, and 128x32 four-bit DMD. Manual geometric switch descriptions that disagree with the working script are retained as manual aliases/locators but do not override the proven table behavior.

## Ball inventory and startup

Create four trough balls and close switches 18, 19, 20, and 21. Leave stack opto 22 open until output 1 moves a ball through the eject end; the script pulses 22 when another ball remains. Initialize the cannon empty at home with switch 61 active and 62 inactive. The bell contains a captive steel ball that is part of its pendulum assembly, not a playable trough ball. The lower mini-playfield eject and both saucers start empty.

## Ball paths

Output 2 launches from switch 23. The main playfield includes left and right orbits, left and right ramps, three top lanes, the Jukebox/top saucer at switch 37, the bell eject at 36, and the cannon capture at 45. The right-ramp diverter routes a ball either through the normal ramp or into the cannon. The left-ramp diverter selects the ordinary return or crossover path. The lower mini-playfield has its own two flippers, three standups, two rollovers, and eject opto 49; output 3 returns its held ball.

## Custom mechanisms

The cannon motor sweeps a ball-holding cannon from about 110 degrees home toward 20 degrees and back. Switch 61 is home, switch 62 is the ROM timing mark, and public output 53 fires at the current angle. The swinging bell must transfer collision momentum into the captive ball and pendulum, report a score excursion on switch 47, and accept magnet output 54 during the Hells Bells feature. Public output 51 animates the linked band members. Output 18 actuates the detonator handle independently of target switch 46. Outputs 6 and 7 reset the five-bank AC/DC and three-bank TNT drop targets.

## Lamps and flashers

Standard lamps 1-80 are the manual matrix. Public lamps 81-128 are tri-color LED channels; each three-address group is blue, green, red as proven by the VPX script. Addresses 114-116 and 129 are unused. Color-GI channels 130, 132, 134, and 136 arrive through ChangedLamps and drive red, blue, lower-playfield, and white GI respectively; GI 0 remains a separate emulator-level channel. Flame-tunnel LEDs are 151-158. Local VPX array indices 177, 179, 180, 182, 183, and 185-190 are solenoid-flasher mirrors, not physical PinMAME lamp outputs, and must never be recreated as duplicate lamps.

## Auxiliary output translation

The manual's physical auxiliary coils 41-48 appear through LibPinMAME as public solenoids 51-58. Therefore physical 41 band members is public 51, physical 42 bell eject is 52, physical 43 cannon eject is 53, physical 44 bell magnet is 54, physical 45 right-ramp diverter is 55, physical 46 right control gate is 56, physical 47 left-ramp diverter is 57, and physical 48 is unused/public 58.

## Cabinet and service inputs

The main flipper buttons/EOS contacts are public switches 84/83 and 82/81. Lower mini-playfield buttons are public 88 and 86; 87 and 85 are unused. Matrix switch 64 is the FIRE button. Negative public switch addresses are the coin-door and tilt inputs after PinMAME inversion normalization; do not apply physical NC inversion twice.

PinMAME public solenoid 33 is the synthetic SAM game-on/fast-flip state and has no physical transistor. The manual's optional ticket-service identities 33-35 are retained separately under `physical.output.ticket`; the stable LibPinMAME solenoid API does not transport them.

## Timing and tuning

The working table's exact impulses are implementation evidence rather than universal geometry: auto-launch uses roughly 55 strength, bell eject 8, cannon eject 45, and the top eject has a special high-power PWM path for the super skill shot. Preserve the causal state changes first, then tune physical travel in the target engine while retaining the switch/output ordering.

## Evidence

- Official Premium manual SHA-256 d3de500b504b165023e3858883067ca518543307387ec2460397b740ebe240b6 and LUCI manual SHA-256 65bb776389508259513cb72f4c24f054f97dfaa0eee87557a0f76e3175acf524 are organized under E:/_vpe-2025/pinmame-manuals.
- Working LUCI script SHA-256 b478b21272befd41908aa3ef4daf3a90d4838334346718cb4d5fde7f23bb2fc0 comes from pinned vpxtable_scripts revision 0c036bb61b4b4e8c778c37559f6795df8cd1521e.
- Exact acd_170h boot/start evidence SHA-256 31d6c8a83091c62785ce5b23cb1417a12bfb229ed61b5366354451510e4940c0; ROM archive SHA-256 1ace847619af4864769b053f641d3e035a1c72d517ac750af7088600cdd291d4 remains external.
