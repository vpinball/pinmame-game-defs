# Williams Black Knight (game 500) — Playfield Switch Wiring Diagram

Source: `Williams_1980_Black_Knight_English_Manual_with_paginated_schematics.pdf` (IPDB 310),
PDF page 68, printed page `24`, sheet marked `500`. The sheet is a landscape scan; its caption, printed page number and
sheet number run sideways, but the drawing itself reads upright in the unrotated landscape render (`man600-68.png`), so
no rotation was applied for reading. Transcribed by hand from the 600 dpi render, cross-checked against the 300 dpi colour
copy (`Williams_1980_Black_Knight_Schematic_Diagrams_paginated.pdf`, PDF page 21), which carries handwritten pen marks
(for example a note `1N4001 diode` and scribbles near 8SW37-8SW46 and 8D45/8D46) that are not part of the printed drawing and are ignored here.

Heading, verbatim: `BLACK KNIGHT` / `PLAYFIELD SWITCH WIRING DIAGRAM` (title above the matrix); italic caption
`Playfield Switch Wiring Diagram`; printed page number `24`; sheet number `500`.

Normalizations: none to spelling or wire colours. Drawing conventions: column wires are the vertical lines (entering from
the top), row wires are the horizontal lines (entering from the left). Each matrix cell is a switch symbol (the designator
`8SWnn` printed to its upper left, open blade drawn) with its diode in series on a diagonal below it; the switch's upper-right
end is on the vertical column wire to its right, the diode's lower-left end is on the horizontal row wire beneath it. The diode
symbol is drawn with the bar at its upper-right (switch-side) end and the triangle pointing up-right toward the bar, for every
diode on this sheet (this is the opposite way round to the lamp sheet, where the bar is at the row-wire end).

## Left-hand connector chains

### Columns: 2J2 / 2P2 (labelled `PART OF DRIVER BOARD`), 8P1 / 8J1, 8P4 / 8J4
| 2J2 pin | 2P2 wire colour | 8P1 / 8J1 pin | Printed label on 8J1 side | 8P4 / 8J4 pin | Where it goes |
|---|---|---|---|---|---|
| 1 | GRN-GRY | 7 | `N.C.` printed at the 8J1 pin | none | no further connection drawn |
| 2 | GRN-VIO | 6 | `N.C.` printed at the 8J1 pin | none | no further connection drawn |
| 3 | GRN-BLU | 5 | COLUMN 6 | 5 | outermost vertical wire, to switches 8SW41-8SW46 |
| 5 | GRN-BLK | 4 | COLUMN 5 | none; the line is drawn straight between the two 8P4/8J4 bar sections | second vertical wire, to switches 8SW33-8SW39 |
| 6 | GRN-YEL | 3 | COLUMN 4 | 3 | vertical wire to switches 8SW25-8SW31 |
| 7 | GRN-ORN | 2 | COLUMN 3 | 2 | vertical wire to switches 8SW17-8SW24 |
| 8 | GRN-RED | 1 | COLUMN 2 | 1 | innermost vertical wire, to switches 8SW11-8SW16 |

(2J2 pins are printed 1, 2, 3, 5, 6, 7, 8; there is no pin 4 printed. 8P1/8J1 pins are printed 7 down to 1 in that order. The
8P4/8J4 bar is drawn in two sections with jagged ends: pin 5 on the upper section, pins 3, 2, 1 on the lower; no pin 4 is
printed.)

### Rows: 2J3 / 2P3 (labelled `PART OF DRIVER BOARD`), 8P1 / 8J1, 8P4 / 8J4
| 2J3 pin | 2P3 wire colour | 8P1 / 8J1 pin | Printed label | 8P4 / 8J4 pin |
|---|---|---|---|---|
| 9 | WHT-BRN | 8 | ROW 1 | 8 |
| 8 | WHT-RED | 9 | ROW 2 | 9 |
| 7 | WHT-ORN | 10 | ROW 3 | 10 |
| 6 | WHT-YEL | 11 | ROW 4 | 11 |
| 5 | WHT-GRN | 12 | ROW 5 | 12 |
| 4 | WHT-BLU | 13 | ROW 6 | 13 |
| 3 | WHT-VIO | 14 | ROW 7 | 14 |
| 1 | WHT-GRY | 15 | ROW 8 | 15 |

(2J3 pins printed 9, 8, 7, 6, 5, 4, 3, 1; no pin 2.) From the 8J4 bar the eight row wires run left-to-right into the matrix
and each turns to the row line under the diodes of one matrix row; ROW 1 is the topmost matrix row (diodes 8D17, 8D25, 8D33, 8D41),
ROW 8 the bottom one.

## Key printed on the sheet
Grey square key: `INDICATES MOUNTED ON UPPER PLAYFIELD AND ARE NOT ROUTED THROUGH 8P4/8J4.`

## Switch matrix: every switch (8SW11-8SW46) with its diode, column wire, row wire

The matrix has five column wires (COLUMN 2 to COLUMN 6) and eight row wires. The cells actually drawn are listed; positions
with no switch drawn are listed as `(none)` against the legend entry that would occupy that number. Shaded cells in the scan:
8SW14; 8SW33-8SW39; 8SW41-8SW44 (8SW45 and 8SW46 are unshaded).

| Switch | Diode | Printed legend (switch list) | Column wire | Row wire | Shaded |
|---|---|---|---|---|---|
| (none) | (none) | 09 Right Magnet Button | | | **not drawn: no `8SW9` or `8D9` is printed and the matrix cell at COLUMN 2, ROW 1 position is empty** |
| (none) | (none) | 10 Left Magnet Button | | | **not drawn: no `8SW10` or `8D10` is printed and the matrix cell at COLUMN 2, ROW 2 position is empty** |
| 8SW11 | 8D11 | 11 Left Outlane (5,000) | COLUMN 2 (2J2 pin 8, GRN-RED; 8P1/8J1 pin 1; 8P4/8J4 pin 1) | ROW 3 (2J3 pin 7, WHT-ORN; 8P1/8J1 pin 10; 8P4/8J4 pin 10) | no |
| 8SW12 | 8D12 | 12 Right Outlane (5000) | COLUMN 2 (2J2 pin 8, GRN-RED; 8P1/8J1 pin 1; 8P4/8J4 pin 1) | ROW 4 (2J3 pin 6, WHT-YEL; 8P1/8J1 pin 11; 8P4/8J4 pin 11) | no |
| 8SW13 | 8D13 | 13 Spinner (100/2,500*) | COLUMN 2 (2J2 pin 8, GRN-RED; 8P1/8J1 pin 1; 8P4/8J4 pin 1) | ROW 5 (2J3 pin 5, WHT-GRN; 8P1/8J1 pin 12; 8P4/8J4 pin 12) | no |
| 8SW14 | 8D14 | 14 Right Ramp Rollunder (500/Mystery) | COLUMN 2 (2J2 pin 8, GRN-RED; 8P1/8J1 pin 1; 8P4/8J4 pin 1) | ROW 6 (2J3 pin 4, WHT-BLU; 8P1/8J1 pin 13; 8P4/8J4 pin 13) | yes |
| 8SW15 | 8D15 | 15 Right Inside Rollover (2,000/10,000**) | COLUMN 2 (2J2 pin 8, GRN-RED; 8P1/8J1 pin 1; 8P4/8J4 pin 1) | ROW 7 (2J3 pin 3, WHT-VIO; 8P1/8J1 pin 14; 8P4/8J4 pin 14) | no |
| 8SW16 | 8D16 | 16 Left Inside Rollover (2,000/10,000**) | COLUMN 2 (2J2 pin 8, GRN-RED; 8P1/8J1 pin 1; 8P4/8J4 pin 1) | ROW 8 (2J3 pin 1, WHT-GRY; 8P1/8J1 pin 15; 8P4/8J4 pin 15) | no |
| 8SW17 | 8D17 | 17 Right Ball Ramp | COLUMN 3 (2J2 pin 7, GRN-ORN; 8P1/8J1 pin 2; 8P4/8J4 pin 2) | ROW 1 (2J3 pin 9, WHT-BRN; 8P1/8J1 pin 8; 8P4/8J4 pin 8) | no |
| 8SW18 | 8D18 | 18 Center Ball Ramp | COLUMN 3 (2J2 pin 7, GRN-ORN; 8P1/8J1 pin 2; 8P4/8J4 pin 2) | ROW 2 (2J3 pin 8, WHT-RED; 8P1/8J1 pin 9; 8P4/8J4 pin 9) | no |
| 8SW19 | 8D19 | 19 Left Ball Ramp | COLUMN 3 (2J2 pin 7, GRN-ORN; 8P1/8J1 pin 2; 8P4/8J4 pin 2) | ROW 3 (2J3 pin 7, WHT-ORN; 8P1/8J1 pin 10; 8P4/8J4 pin 10) | no |
| 8SW20 | 8D20 | 20 Outhole | COLUMN 3 (2J2 pin 7, GRN-ORN; 8P1/8J1 pin 2; 8P4/8J4 pin 2) | ROW 4 (2J3 pin 6, WHT-YEL; 8P1/8J1 pin 11; 8P4/8J4 pin 11) | no |
| 8SW21 | 8D21 | 21 Left Kicker (10) | COLUMN 3 (2J2 pin 7, GRN-ORN; 8P1/8J1 pin 2; 8P4/8J4 pin 2) | ROW 5 (2J3 pin 5, WHT-GRN; 8P1/8J1 pin 12; 8P4/8J4 pin 12) | no |
| 8SW22 | 8D22 | 22 Right Kicker (10) | COLUMN 3 (2J2 pin 7, GRN-ORN; 8P1/8J1 pin 2; 8P4/8J4 pin 2) | ROW 6 (2J3 pin 4, WHT-BLU; 8P1/8J1 pin 13; 8P4/8J4 pin 13) | no |
| 8SW23 | 8D23 | 23 Turnaround (5,000) | COLUMN 3 (2J2 pin 7, GRN-ORN; 8P1/8J1 pin 2; 8P4/8J4 pin 2) | ROW 7 (2J3 pin 3, WHT-VIO; 8P1/8J1 pin 14; 8P4/8J4 pin 14) | no |
| 8SW24 | 8D24 | 24 Lower Playfield Eject Hole (5,000) | COLUMN 3 (2J2 pin 7, GRN-ORN; 8P1/8J1 pin 2; 8P4/8J4 pin 2) | ROW 8 (2J3 pin 1, WHT-GRY; 8P1/8J1 pin 15; 8P4/8J4 pin 15) | no |
| 8SW25 | 8D25 | 25 Lower Left 3-Bank, Lower Target (1,000) | COLUMN 4 (2J2 pin 6, GRN-YEL; 8P1/8J1 pin 3; 8P4/8J4 pin 3) | ROW 1 (2J3 pin 9, WHT-BRN; 8P1/8J1 pin 8; 8P4/8J4 pin 8) | no |
| 8SW26 | 8D26 | 26 Lower Left 3-Bank, Center Target (1,000) | COLUMN 4 (2J2 pin 6, GRN-YEL; 8P1/8J1 pin 3; 8P4/8J4 pin 3) | ROW 2 (2J3 pin 8, WHT-RED; 8P1/8J1 pin 9; 8P4/8J4 pin 9) | no |
| 8SW27 | 8D27 | 27 Lower Left 3-Bank, Upper Target (1,000) | COLUMN 4 (2J2 pin 6, GRN-YEL; 8P1/8J1 pin 3; 8P4/8J4 pin 3) | ROW 3 (2J3 pin 7, WHT-ORN; 8P1/8J1 pin 10; 8P4/8J4 pin 10) | no |
| (none) | (none) | 28 Lower Left 3-Bank, Standup (10) | | | **not drawn: no `8SW28` or `8D28` is printed and the matrix cell at COLUMN 4, ROW 4 position is empty** |
| 8SW29 | 8D29 | 29 Lower Right 3-Bank, Right Target (1,000) | COLUMN 4 (2J2 pin 6, GRN-YEL; 8P1/8J1 pin 3; 8P4/8J4 pin 3) | ROW 5 (2J3 pin 5, WHT-GRN; 8P1/8J1 pin 12; 8P4/8J4 pin 12) | no |
| 8SW30 | 8D30 | 30 Lower Right 3-Bank, Center Target (1,000) | COLUMN 4 (2J2 pin 6, GRN-YEL; 8P1/8J1 pin 3; 8P4/8J4 pin 3) | ROW 6 (2J3 pin 4, WHT-BLU; 8P1/8J1 pin 13; 8P4/8J4 pin 13) | no |
| 8SW31 | 8D31 | 31 Lower Right 3-Bank, Left Target (1,000) | COLUMN 4 (2J2 pin 6, GRN-YEL; 8P1/8J1 pin 3; 8P4/8J4 pin 3) | ROW 7 (2J3 pin 3, WHT-VIO; 8P1/8J1 pin 14; 8P4/8J4 pin 14) | no |
| (none) | (none) | 32 Lower Right 3-Bank, Standup (10) | | | **not drawn: no `8SW32` or `8D32` is printed and the matrix cell at COLUMN 4, ROW 8 position is empty** |
| 8SW33 | 8D33 | 33 Top Left 3-Bank, Lower Target (1,000) | COLUMN 5 (2J2 pin 5, GRN-BLK; 8P1/8J1 pin 4; 8P4/8J4 pin none (line bypasses 8P4/8J4)) | ROW 1 (2J3 pin 9, WHT-BRN; 8P1/8J1 pin 8; 8P4/8J4 pin 8) | yes |
| 8SW34 | 8D34 | 34 Top Left 3-Bank, Center Target (1,000) | COLUMN 5 (2J2 pin 5, GRN-BLK; 8P1/8J1 pin 4; 8P4/8J4 pin none (line bypasses 8P4/8J4)) | ROW 2 (2J3 pin 8, WHT-RED; 8P1/8J1 pin 9; 8P4/8J4 pin 9) | yes |
| 8SW35 | 8D35 | 35 Top Left 3-Bank, Upper Target (1,000) | COLUMN 5 (2J2 pin 5, GRN-BLK; 8P1/8J1 pin 4; 8P4/8J4 pin none (line bypasses 8P4/8J4)) | ROW 3 (2J3 pin 7, WHT-ORN; 8P1/8J1 pin 10; 8P4/8J4 pin 10) | yes |
| 8SW36 | 8D36 | 36 Jet Bumper (500) | COLUMN 5 (2J2 pin 5, GRN-BLK; 8P1/8J1 pin 4; 8P4/8J4 pin none (line bypasses 8P4/8J4)) | ROW 4 (2J3 pin 6, WHT-YEL; 8P1/8J1 pin 11; 8P4/8J4 pin 11) | yes |
| 8SW37 | 8D37 | 37 Top Right 3-Bank, Lower Target (1,000) | COLUMN 5 (2J2 pin 5, GRN-BLK; 8P1/8J1 pin 4; 8P4/8J4 pin none (line bypasses 8P4/8J4)) | ROW 5 (2J3 pin 5, WHT-GRN; 8P1/8J1 pin 12; 8P4/8J4 pin 12) | yes |
| 8SW38 | 8D38 | 38 Top Right 3-Bank, Center Target (1,000) | COLUMN 5 (2J2 pin 5, GRN-BLK; 8P1/8J1 pin 4; 8P4/8J4 pin none (line bypasses 8P4/8J4)) | ROW 6 (2J3 pin 4, WHT-BLU; 8P1/8J1 pin 13; 8P4/8J4 pin 13) | yes |
| 8SW39 | 8D39 | 39 Top Right 3-Bank, Upper Target (1,000) | COLUMN 5 (2J2 pin 5, GRN-BLK; 8P1/8J1 pin 4; 8P4/8J4 pin none (line bypasses 8P4/8J4)) | ROW 7 (2J3 pin 3, WHT-VIO; 8P1/8J1 pin 14; 8P4/8J4 pin 14) | yes |
| (none) | (none) | 40 Top Right 3-Bank, Standup (10) | | | **not drawn: no `8SW40` or `8D40` is printed and the matrix cell at COLUMN 5, ROW 8 position is empty** |
| 8SW41 | 8D41 | 41 Lockup Trough, Bottom (5,000‡) | COLUMN 6 (2J2 pin 3, GRN-BLU; 8P1/8J1 pin 5; 8P4/8J4 pin 5) | ROW 1 (2J3 pin 9, WHT-BRN; 8P1/8J1 pin 8; 8P4/8J4 pin 8) | yes |
| 8SW42 | 8D42 | 42 Lockup Trough, Center (5,000‡) | COLUMN 6 (2J2 pin 3, GRN-BLU; 8P1/8J1 pin 5; 8P4/8J4 pin 5) | ROW 2 (2J3 pin 8, WHT-RED; 8P1/8J1 pin 9; 8P4/8J4 pin 9) | yes |
| 8SW43 | 8D43 | 43 Lockup Trough, Top (5,000‡) | COLUMN 6 (2J2 pin 3, GRN-BLU; 8P1/8J1 pin 5; 8P4/8J4 pin 5) | ROW 3 (2J3 pin 7, WHT-ORN; 8P1/8J1 pin 10; 8P4/8J4 pin 10) | yes |
| 8SW44 | 8D44 | 44 Left Ramp Rollover (5,000) | COLUMN 6 (2J2 pin 3, GRN-BLU; 8P1/8J1 pin 5; 8P4/8J4 pin 5) | ROW 4 (2J3 pin 6, WHT-YEL; 8P1/8J1 pin 11; 8P4/8J4 pin 11) | yes |
| 8SW45 | 8D45 | 45 Ballshooter Trough | COLUMN 6 (2J2 pin 3, GRN-BLU; 8P1/8J1 pin 5; 8P4/8J4 pin 5) | ROW 5 (2J3 pin 5, WHT-GRN; 8P1/8J1 pin 12; 8P4/8J4 pin 12) | no |
| 8SW46 | 8D46 | 46 Playfield Tilt | COLUMN 6 (2J2 pin 3, GRN-BLU; 8P1/8J1 pin 5; 8P4/8J4 pin 5) | ROW 6 (2J3 pin 4, WHT-BLU; 8P1/8J1 pin 13; 8P4/8J4 pin 13) | no |

## Printed switch list (right edge of sheet), verbatim
Headed `Switch` / `No.` and `Function (Score)`; transcribed in the table above. Footer notes, verbatim:

- `Note: Second value is lit or flashing value`
- `* Spinner lit for interval after making right inside rollover` / `Mystery is 20,000 - 99,000 and lit for interval after making left inside rollover`
- `** Inside rollovers light when made after using Magna-Save feature` (`Magna-Save` printed in italics)
- `‡ Only one lockup trough switch scores for each locked-up ball`

## Observations
- Switch numbers `09` and `10` (Right Magnet Button, Left Magnet Button) are in the printed list but no switch is drawn for
  them on this sheet (COLUMN 2, ROW 1 and ROW 2 positions are empty).
- Standups: `28 Lower Left 3-Bank, Standup (10)`, `32 Lower Right 3-Bank, Standup (10)` and `40 Top Right 3-Bank, Standup (10)`
  appear in the printed list, but no `8SW28`, `8SW32` or `8SW40` (and no diode) is drawn; the cells at COLUMN 4 ROW 4, COLUMN 4
  ROW 8 and COLUMN 5 ROW 8 are empty. The lower-left/lower-right 3-bank target switches 8SW25-8SW27 and 8SW29-8SW31 and the top-left /
  top-right 3-bank target switches 8SW33-8SW35 and 8SW37-8SW39 are drawn.
- `36 Jet Bumper (500)` is drawn as an ordinary matrix switch `8SW36` (COLUMN 5, ROW 4, diode 8D36, shaded).
- No switch on this sheet is labelled `NOT USED`.
- Column wire for switches 8SW41-8SW46 (COLUMN 6) is drawn through 8P4/8J4 pin 5. The key says shaded cells are "not routed
  through 8P4/8J4": the shaded switches 8SW41-8SW44 share that COLUMN 6 wire (and ROW 1-4 wires, which are drawn through
  8P4/8J4 pins 8-11) with the unshaded 8SW45 and 8SW46; likewise the shaded 8SW14 shares COLUMN 2 (8P4/8J4 pin 1) and
  ROW 6 (pin 13) with unshaded switches. COLUMN 5 (8SW33-8SW39, all shaded) is the only column drawn without an 8P4/8J4
  pin. Recorded as drawn.
- 8SW45 (Ballshooter Trough) and 8SW46 (Playfield Tilt) sit at COLUMN 6 ROW 5 and ROW 6, to the right of the shaded block.
- Pins printed `N.C.`: 8J1 pins 7 and 6 (2J2 pins 1 and 2, GRN-GRY and GRN-VIO).
- The diode designators equal the switch numbers (8D11-8D46, none for the undrawn positions).

## Illegible / uncertain items
None. Shading partly obscures the labels of 8SW33, 8SW34, 8SW35, 8SW36, 8SW41-8SW44 and 8D33-8D44 in the 600 dpi scan, but all
read unambiguously and are consistent with the colour copy.
