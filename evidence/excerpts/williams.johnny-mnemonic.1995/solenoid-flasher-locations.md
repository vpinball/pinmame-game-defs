# Williams Johnny Mnemonic (1995) — Solenoid/Flashlamp Locations

Source: Williams *Johnny Mnemonic* operations manual (September 1995), IPDB machine 3683 file
`Williams_1995_Johnny_Mnemonic_English_Manual.pdf`, PDF page 105, printed page 2-37. Read from the
native 300 dpi render (`p-105.png`, 2550 x 3300 px). The page carries a parts list on the left and a
numbered playfield drawing on the right; this transcription covers both and is cited by two crops,
`solenoid-flasher-locations` (the list) and `solenoid-flasher-locations-drawing` (the drawing).

## Parts list

Columns: Item No. | Coil/Flasher No. | Assembly No. | Description. `---------` is printed in the
assembly column where it is shown here.

| Item | Coil/Flasher | Assembly | Description |
| --- | --- | --- | --- |
| 01 | AE-26-1500 | A-19963 | Trough Eject |
| 02 | AE-23-800 | A-14525 | Autoplunger |
| 03 | AE-24-900 | A-20498 | Popper |
| 04 | (blank) | (blank) | Not Used |
| 05 | AE-25-1000 | A-20446 | Clear Matrix |
| 06 | 20-10201 | A-20500 | Hand Magnet |
| 07 | AE-23-800 | A-10686-1 | Knocker\*\* |
| 08 | (blank) | (blank) | Not Used |
| 09 | AE-26-1200 | B-9362-L-2 | Left Slingshot |
| 10 | AE-26-1200 | B-9362-R-3 | Right Slingshot |
| 11 | AE-26-1200 | A-9415-2 | Left Jet Bumper |
| 12 | AE-26-1200 | A-9415-2 | Bottom Jet Bumper |
| 13 | AE-26-1200 | A-9415-2 | Right Jet Bumper |
| 14 | AE-26-1500 | A-20496 | Crazy Bob's Eject |
| 15 | AE-26-1200 | A-20587 | Drop Target Up |
| 16 | SM1-26-600 | A-20587 | Drop Target Down |
| 17 | 24-8704 | A-17803 | Jet Flasher |
| 18 | 24-8802 | A-17802 | Crazy Bob's Flasher |
| | 24-8802 | --------- | Inset Panel |
| 19 | 24-8802 | --------- | Left Slingshot Flasher\* |
| 20 | 24-8802 | --------- | Right Slingshot Flashr\* |
| | 24-8802 | --------- | Insert Panel |
| 21 | 14-8025 | A-20532 | "X" Motor Direction |
| 22 | 14-8025 | A-20532 | "X" Motor Enable |
| 23 | 14-8025 | A-20532 | "Y" Motor Direction |
| 24 | 14-8025 | A-20532 | "Y" Motor Enable |
| 25 | 24-8802 | --------- | Left Ramp Flasher\* |
| | 24-8802 | --------- | Insert Panel |
| 26 | 24-8802 | --------- | Right Ramp Flasher\* |
| 27 | 24-8704 | 04-10280 | Hand Popper Flasher |
| 28 | 24-8802 | --------- | Right Back Panel Flsr |
| | 24-8802 | --------- | Insert Panel |

Flippers:

| Item | Coil/Flasher | Assembly | Description |
| --- | --- | --- | --- |
| 29-30 | FL-11629 | A-19223-R | Lower Right Flipper |
| 31-32 | FL-11629 | A-15849-L-2 | Lower Left Flipper |
| 33-34 | FL-11753 | A-20497 | Left Diverter |
| 35-36 | FL-11753 | A-20497 | Right Diverter |

General Illumination:

| Item | Bulb No. | Description |
| --- | --- | --- |
| 01 | 24-6549/24-8768 | String 1 |
| 02 | 24-6549/24-8768 | String 2 |
| 03 | 24-6549/24-8768 | String 3 |
| 04 | 24-6549 | String 4 |
| 05 | 24-8768 | String 5 |

Footer: `24-6549 = #44 BULB`, `24-8704 = #89 BULB`, `24-8768 = #555 BULB`, `24-8802 = #906 BULB`,
`*USED WITH A-14266-13, RECEPTACLE AND SKIRT.`, `**NOT SHOWN`.

The 18 insert-panel row prints `Inset Panel`; the 20, 25 and 28 rows print `Insert Panel`. Those four
rows are the backbox bulbs that the solenoid table gives backbox connections (J125-2, J125-5,
J124-1, J124-5).

## Drawing

Callouts drawn: 01, 02, 03, 05, 06, 09, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24,
26, 27, 28, 33, 34. No callout is drawn for 04, 07 (the list marks the knocker `**NOT SHOWN`), 08,
25, 29-32 or 35-36.

- 11 and 13 are drawn inside the upper-left and right jet bumper rings of the bumper group; 12 is
  the lower bumper. 17 is the plain circle drawn between the two upper bumpers.
- 09 and 10 point at the slingshot kicker assemblies; 19 and 20 at the circles drawn inside the
  left and right slingshots.
- 14 and 18 point at the Crazy Bob's eject box at the centre left, 18 at its upper right corner.
- 26 is the circle drawn at the right of the upper playfield, beside the right loop; 28 points at
  the right end of the back panel; 05 at the right rear corner of the matrix; 27 and 03 into the
  popper mechanism at the rear left, 06, 21, 22, 23 and 24 into the hand drive at the rear left, 15
  and 16 at the drop target beside the popper.
- 33 points at the diverter at the top of the left orbit; 34 at the rear-left rail above it.
- An unlabelled plain dome circle is drawn at the far left of the playfield beside the jet bumpers,
  centred at pixel (1585, 1116), (0.061, 0.287) through the fit below. No callout names it; the
  definition takes it to be the Left Ramp Flasher (25), which has no callout, because a second table
  drives its solenoid-25 glow at the same spot.
- 01 points at the trough under the right of the apron and 02 at the foot of the shooter lane.

The flasher placements in the definition map these callouts through a least-squares affine fit of
this render onto the retained VPX table, using nine shared features (the four corner matrix holes,
the two upper jet bumper centres, both flipper pivots and the Crazy Bob's eject box). The fit, its
pixel readings and its residuals (worst 0.013 normalized) are retained as
`external:pinmame-review-artifacts/johnny-mnemonic/fit_solenoid_drawing.py` and its output. The
control points span x 0.18-0.79 and y 0.06-0.85, so flashers 26 and 28 (x about 0.94) and 28's rear
edge position (y 0.05) are extrapolated and the residual does not bound their error. Coil callouts
measured through the same fit (their pixel readings are in the artifact): 01 ends 0.051 from the
trough eject kicker, 02 0.003 from the autoplunger trigger, 05 on the coil at the matrix's right rear
corner (0.828, 0.038; extrapolated like 26 and 28) and 33 0.060 from the left diverter walls; the
other coil leaders were not measured.
