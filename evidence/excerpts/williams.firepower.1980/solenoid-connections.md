# Williams Firepower (game 497) — Table 3, Solenoid Connections

Source: `Williams_1980_Firepower_Instruction_Booklet.pdf` (IPDB 856, Instruction Booklet
16P-497-103, January 1980), PDF page 9, printed page 9. Transcribed by hand from a native-resolution
render. Every row and every column is written down, including the `--` cells.

Heading, verbatim: `Table 3. Solenoid Connections`.

| SOL. NO. | FUNCTION | WIRE COLOR | CONNECTIONS | DRIVER TRANS. | SOLENOID PART NO. |
| --- | --- | --- | --- | --- | --- |
| 01 | Ball Release | GRY-BRN | 2P11-4, 8P3-17 | Q15 | SA-23-850-DC |
| 02 | Not Used | GRY-RED | 2P11-5, 8P3-18 | Q17 | -- |
| 03 | Not Used | GRY-ORN | 2P11-7, 8P3-19 | Q19 | -- |
| 04 | Left Eject Hole | GRY-YEL | 2P11-8, 8P3-20 | Q21 | SG-23-850-DC |
| 05 | Right Eject Hole | GRY-GRN | 2P11-9, 8P3-21 | Q23 | SG-23-850-DC |
| 06 | Upper Right Eject Hole | GRY-BLU | 2P11-3, 8P3-22 | Q25 | SG-23-850-DC |
| 07 | Left Ball Saver Kicker | GRY-VIO | 2P11-2, 8P3-23 | Q27 | SG-23-850-DC |
| 08 | Ball Ramp Thrower | GRY-BLK | 2P11-1, 8P3-24 | Q29 | SA-23-850-DC |
| 09 | Sound | BRN-BLK | 2P9-9, 10P3-3 | Q31 | -- |
| 10 | Sound | BRN-RED | 2P9-7, 10P3-2 | Q33 | -- |
| 11 | Sound | BRN-ORN | 2P9-1, 10P3-5 | Q35 | -- |
| 12 | Sound | BRN-YEL | 2P9-2, 10P3-4 | Q37 | -- |
| 13 | Sound | BRN-GRN | 2P9-3, 10P3-7 | Q39 | -- |
| 14 | Credit Knocker | BRN-BLU | 2P9-4, 7P1-16 | Q41 | SA2-23-850-DC |
| 15 | Flash Lamps | BRN-VIO | 2P9-5, 6P2 | Q43 | Type 89 Bulbs |
| 16 | Coin Lockout | BRN-GRY | 2P9-6, 7P1-18, 7P2-4 | Q45 | SM-35-4000-DC |
| *17 | Top Left Jet Bumper | BLU-BRN | 2P12-7, 8P3-11 | Q2 | SG-23-850-DC |
| *18 | Bottom Left Jet Bumper | BLU-RED | 2P12-4, 8P3-12 | Q4 | SG-23-850-DC |
| *19 | Top Right Jet Bumper | BLU-ORN | 2P12-3, 8P3-13 | Q6 | SG-23-850-DC |
| *20 | Bottom Left Jet Bumper | BLU-YEL | 2P12-6, 8P3-14 | Q8 | SG-23-850-DC |
| *21 | Right Kicker | BLU-GRN | 2P12-8, 8P3-15 | Q10 | SG-23-850-DC |
| *22 | Left Kicker | BLU-BLK | 2P12-9, 8P3-16 | Q12 | SG-23-800-DC |
| * | Right Flipper | BLU-VIO | 7P1-8, 8P3-3 | -- | SFL-19-400/30-750-DC |
| * | Left Flipper | BLU-GRY | 7P1-10, 8P3-4 | -- | SFL-19-400/30-750-DC |

Row 20 is printed `Bottom Left Jet Bumper`, the same function text as row 18. On this scan a
previous owner has pencilled `Rt` across the wire-colour cell of row 20 and a mark beside the
number of row 18; those marks are handwriting, not print. The playfield solenoid wiring diagram
(schematics page 25) labels the coil on this circuit `8L20 BOTTOM RIGHT JET BUMPER`, Figure 3
places callout `20` on the bottom right bumper, and the switch named by pinned PinMAME's
`sxx.ssSw` for special solenoid 20 is matrix switch 28, `BOTTOM RIGHT JET BUMPER`. Row 20's
printed text is therefore a typing error for Bottom Right Jet Bumper.

Row 22's part number is printed `SG-23-800-DC` where rows 17 to 21 print `SG-23-850-DC`.

## Notes block, verbatim

`*NOTES:`

1. `Special switch connections for solenoids 17 through 22 are as follows:`

   | Solenoid | Wire | Connections |
   | --- | --- | --- |
   | 17 | ORN-BRN | 2P13-5, 8P3-5 |
   | 18 | ORN-RED | 2P13-3, 8P3-6 |
   | 19 | ORN-BLK | 2P13-2, 8P3-7 |
   | 20 | ORN-YEL | 2P13-4, 8P3-8 |
   | 21 | ORN-GRN | 2P13-8, 8P3-9 |
   | 22 | ORN-BLU | 2P13-9, 8P3-10 |

2. `Flipper button connections are as follows:`

   `Right -- ORN-VIO -- 2P12-1, 7P1-7`

   `Left -- ORN-GRY -- 2P12-2, 7P1-9`

3. `Typical wiring for solenoids and special switches:` a drawing of a coil with a diode across it
   between two lines, the upper line labelled `RED (B+)`, and below it a switch with a resistor and
   capacitor in series across it, on a line labelled `BLK (GRD)`.
