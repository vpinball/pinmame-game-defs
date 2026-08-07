# Flash Gordon - Auxiliary Lamp Driver A9 (AS-2518-52)

Transcribed from `Flash Gordon Bally 1981 English Manual.pdf`, PDF page 55, drawing `W-1207-5C`,
titled `AUXILIARY LAMP DRIVER "A9"`, material code `FLASH GORDON`, game `#1215`, drawn 11-17-80 and
approved 11-19-80. Read from a 400 dpi `pdftoppm` render. The accompanying crop is the decoder / SCR
/ connector block, grayscale, because a fan-out is a drawing rather than a table.

The board carries four `MC14028B` (`E-620-108`) BCD-to-decimal decoders U2 through U5, twenty-eight
`MCR-106` SCRs (`E-585-29`) Q1 through Q28 each behind a 2K resistor, and a quad flip-flop U1
(`E-620-134`). Seven outputs of each decoder are used and output 7 of each is wired to `N/U`, which
is why the board has 4 x 7 = 28 circuits and not 4 x 8. The board-layout page (PDF page 39) lists the
same part complement: `Q1 Thru Q28` S.C.R., `U2 Thru U5` BCD to Decimal Decoder, `R10 Thru R37` 2K.

**Deliberately not transcribed, because it is not on the retained scan:** the A / B / C / D-bar input
stubs on the left edge of each decoder run off the page margin, so which lamp data line enables which
decoder cannot be read from this sheet. The decoder-to-data-line order this definition uses is the
printed order U2, U3, U4, U5, which the retained known-working table's own address bindings
corroborate on seventeen of the eighteen circuits it drives.

## Decoder outputs, SCRs and connector pins

| Decoder | Output | SCR | Connector pin | Printed function |
| --- | --- | --- | --- | --- |
| U2 | 0 | Q1 | A9J2-7 | UPPER TOP RT. R.O. BUTTON |
| U2 | 1 | Q2 | A9J2-4 | 1 FLASH GORDON |
| U2 | 2 | Q3 | A9J2-8 | 4 FLASH GORDON |
| U2 | 3 | Q4 | A9J2-10 | FACE OF MING |
| U2 | 4 | Q5 | A9J2-9 | 3X 15 SECOND CLOCK |
| U2 | 5 | Q6 | A9J2-6 | N/U |
| U2 | 6 | Q7 | A9J2-5 | N/U |
| U3 | 0 | Q8 | A9J2-14 | TOP SHOOTER ALLEY R.O. BUTTON |
| U3 | 1 | Q9 | A9J2-11 | 2 FLASH GORDON |
| U3 | 2 | Q10 | A9J2-15 | 5 FLASH GORDON |
| U3 | 3 | Q11 | A9J2-18 | FACE OF MING |
| U3 | 4 | Q12 | A9J2-17 | 2X 15 SECOND CLOCK |
| U3 | 5 | Q13 | A9J2-13 | N/U |
| U3 | 6 | Q14 | A9J2-12 | N/U |
| U4 | 0 | Q15 | A9J3-8 | MIDDLE SHOOTER ALLEY R.O. BUTTON |
| U4 | 1 | Q16 | A9J3-3 | 3 FLASH GORDON |
| U4 | 2 | Q17 | A9J3-9 | 6 FLASH GORDON |
| U4 | 3 | Q18 | A9J3-11 | N/U |
| U4 | 4 | Q19 | A9J3-10 | 3X SAUCER ARROW |
| U4 | 5 | Q20 | A9J3-7 | N/U |
| U4 | 6 | Q21 | A9J3-4 | N/U |
| U5 | 0 | Q22 | A9J3-15 | LOWER SHOOTER ALLEY R.O. BUTTON |
| U5 | 1 | Q23 | A9J3-12 | N/U |
| U5 | 2 | Q24 | A9J3-16 | N/U |
| U5 | 3 | Q25 | A9J3-18 | BACK BOX STROBE |
| U5 | 4 | Q26 | A9J3-17 | 2X SAUCER ARROW |
| U5 | 5 | Q27 | A9J3-14 | N/U |
| U5 | 6 | Q28 | A9J3-13 | N/U |

Seventeen of the twenty-eight circuits carry a function and eleven are `N/U`.

Also printed on the connector bodies: A9J2 pins 1 and 2 are `N/U` and pin 3 is `KEY`; A9J3 pins 1
and 2 are `N/U` and `KEY`, and pins 5, 6, 19 and 20 are `GND`.

## A9 harness plug tables printed on the same sheet

Wire-colour codes for the pins the harness actually plugs. A pin printed `N/U` here carries no wire.

A9 J2, headed `TO PANEL W-1192-26C`:

| Pin | Wire |
| --- | --- |
| 1 | N/U |
| 2 | N/U |
| 3 | KEY |
| 4 | 15 |
| 5 | N/U |
| 6 | N/U |
| 7 | 10 |
| 8 | 51 |
| 9 | 54 |
| 10 | 80 |
| 11 | 18 |
| 12 | N/U |
| 13 | N/U |
| 14 | 12 |
| 15 | 52 |
| 16 | N/U |
| 17 | 43 |
| 18 | 57 |

A9 J3, headed `TO INSERT`:

| Pin | Wire |
| --- | --- |
| 1 | N/U |
| 2 | KEY |
| 3 | 20 |
| 4 | N/U |
| 5 | N/U |
| 6 | N/U |
| 7 | N/U |
| 8 | 13 |
| 9 | 53 |
| 10 | 25 |
| 11 | N/U |
| 12 | N/U |
| 13 | N/U |
| 14 | N/U |
| 15 | 14 |
| 16 | N/U |
| 17 | 15 |
| 18 | 72 |
| 19 | N/U |
| 20 | N/U |

The two tables agree with the connector-function column pin for pin: every pin printed `N/U` on the
board block is also `N/U` in the plug table, and every pin with a function carries a wire. A9J3-11 is
`N/U` in both places, which is what makes the retained table's use of that circuit a genuine
disagreement rather than a transcription slip.
