# Williams Black Knight (game 500) — Playfield Lamp Wiring Diagram

Source: `Williams_1980_Black_Knight_English_Manual_with_paginated_schematics.pdf` (IPDB 310),
PDF page 66, printed page `22`, sheet marked `500`. The sheet is a landscape scan; its caption, printed page number and
sheet number run sideways, but the drawing itself reads upright in the unrotated landscape render (`man600-66.png`), so
no rotation was applied for reading. Transcribed by hand from the 600 dpi render, cross-checked against the 300 dpi colour
copy (`Williams_1980_Black_Knight_Schematic_Diagrams_paginated.pdf`, PDF page 20, left half), which carries
handwritten pen marks that are not part of the printed drawing and are ignored here.

Heading, verbatim: `BLACK KNIGHT` / `PLAYFIELD LAMP WIRING DIAGRAM` (drawing title above the matrix); italic caption
`Playfield Lamp Wiring Diagram` (left margin, sideways); printed page number `22`; sheet number `500`.

Normalizations: none to spelling or wire colours (`YEL-GRY`, `RED-BRN`, `VIO`, `WHT`, `YEL-WHT` kept literal). The matrix is
drawn with column wires entering from the top (vertical) and row wires entering from the left (horizontal). Every bulb is
drawn as a lamp symbol with its diode in series on a diagonal: the bulb end (upper right) is on the vertical column wire, the
diode's lower-left end is on the horizontal row wire; the diode triangle points down-left (toward the row wire, bar at the
row-wire end) for every bulb. The bulb list printed at the right edge of the sheet (headed `Bulb No.` / `Function`) is
transcribed below; "Magna-Save" is printed in italics in that list.

## Left-hand connector chains

### Columns: 2J5 / 2P5 (labelled `PART OF DRIVER BOARD`, brace on the arrows), 8P2 / 8J2, 8P5 / 8J5
| 2J5 pin | 2P5 wire colour | 8P2 / 8J2 pin | Printed label | 8P5 / 8J5 pin | Where it goes |
|---|---|---|---|---|---|
| 2 | YEL-GRY | 10 | COLUMN 8 | 10 | vertical wire to bulbs 8B57-8B64 |
| 1 | YEL-VIO | 9 | COLUMN 7 | 9 | vertical wire to bulbs 8B49-8B56 |
| 5 | YEL-BLU | 8 | COLUMN 6 | 8 | vertical wire to bulbs 8B41-8B48 |
| 3 | YEL-GRN | 7 | COLUMN 5 | no 8P5/8J5 pin; the line is drawn straight through between the two 8P5/8J5 bar sections | vertical wire to bulbs 8B33-8B40 |
| 7 | YEL-BLK | 6 | COLUMN 4 | 6 | vertical wire to bulbs 8B25-8B32 |
| 6 | YEL-ORN | 5 | COLUMN 3 | 5 | vertical wire to bulbs 8B17-8B24 |
| 9 | YEL-RED | 4 | COLUMN 2 | 4 | vertical wire to bulbs 8B9-8B16 |
| 8 | YEL-BRN | 3 | COLUMN 1 | 3 | printed `NC` (the line from 8J5 pin 3 ends at the text `NC`; no bulb column is drawn) |

The 8P5/8J5 bar is drawn in two sections (pins 10, 9, 8 on the upper section; pins 6, 5, 4, 3 and then the row pins on the
lower section), with a jagged end on each where they meet; the COLUMN 5 line runs between them.

### Rows: 2J7 / 2P7 (labelled `PART OF DRIVER BOARD`, brace on the arrows), 8P2 / 8J2, 8P5 / 8J5
| 2J7 pin | 2P7 wire colour | 8P2 / 8J2 pin | Printed label | 8P5 / 8J5 pin | Where it goes |
|---|---|---|---|---|---|
| 1 | RED-BRN | 11 | ROW 1 | 11 | horizontal row wire, top row (bulbs 8B9, 8B17, ... 8B57) |
| 2 | RED-BLK | 12 | ROW 2 | 12 | second row (8B10, 8B18, ... 8B58) |
| 3 | RED-ORN | 13 | ROW 3 | 13 | third row (8B11, 8B19, ... 8B59) |
| 4 | RED-YEL | 14 | ROW 4 | 14 | fourth row (8B12, 8B20, ... 8B60) |
| 5 | RED-GRN | 15 | ROW 5 | 15 | fifth row (8B13, 8B21, ... 8B61) |
| 6 | RED-BLU | 16 | ROW 6 | 16 | sixth row (8B14, 8B22, ... 8B62) |
| 9 | RED-VIO | 17 | ROW 7 | 17 | seventh row (8B15, 8B23, ... 8B63) |
| 8 | RED-GRY | 18 | ROW 8 | 18 | bottom row (8B16, 8B24, ... 8B64) |

(2J7 pins are printed in the order 1, 2, 3, 4, 5, 6, 9, 8 and 2J5 pins in the order 2, 1, 5, 3, 7, 6, 9, 8; both as shown.)

### General illumination (6.3 VAC)
Small connector pair `8J8` / `8P8` at lower left, brace label `6.3 VAC GENERAL ILLUMINATION`:
| 8J8 wire (colour as printed) | 8J8 pin | 8P8 pin | Further connection drawn |
|---|---|---|---|
| YEL (dotted line) | 5 | (arrow stub, no pin number printed on the 8P8 side beyond the line) | none; the line ends at the 8P8 arrow |
| YEL-WHT (dotted line) | 2 | (arrow stub) | none; the line ends at the 8P8 arrow |
| VIO (solid line) | 1 | (arrow stub) | solid wire to 8P2 pin 1 |
| WHT (solid line) | 4 | (arrow stub) | solid wire to 8P2 pin 2 |

(The 8P8 side prints the numbers `5`, `2`, `1`, `4` between the two bars; the two dotted wires carry arrowheads but no onward wire.)

General illumination drawing: 8P2 / 8J2 pin `1` and pin `2` feed two horizontal lines (an upper line from pin 1, a lower line
from pin 2). Two lamp symbols (no designator printed) are connected across the two lines between 8P2/8J2 and 8P5/8J5. The
lines then pass through 8P5 / 8J5 pins `1` and `2` and continue with two more lamp symbols (no designators), then
continue as dashed lines with two further lamp symbols drawn with dashed connections, then the label
`GENERAL ILLUMINATION`. Six lamp symbols are drawn in total, none with a designator.

## Key printed on the sheet
Grey square key: `INDICATES MOUNTED ON UPPER PLAYFIELD AND CONNECTIONS ARE NOT ROUTED THROUGH 8P5/8J5.`

## Bulb matrix: every bulb (8B9-8B64) with its diode, column wire, row wire

Bulbs 8B1-8B8 are not drawn on this sheet (see the master display sheet). The matrix has seven column groups (COLUMN 2
to COLUMN 8) of eight rows each. Shaded cells in the scan: 8B19, 8B20, 8B21; all of 8B33-8B40; 8B41, 8B42.

| Bulb | Diode | Printed legend (bulb list) | Column wire | Row wire | Shaded cell |
|---|---|---|---|---|---|
| 8B9 | 8D73 | 09 Right Magna-Save | COLUMN 2 (2J5 pin 9, YEL-RED; 8P2/8J2 pin 4; 8P5/8J5 pin 4) | ROW 1 (2J7 pin 1, RED-BRN; 8P2/8J2 pin 11; 8P5/8J5 pin 11) | no |
| 8B10 | 8D74 | 10 Left Magna-Save | COLUMN 2 (2J5 pin 9, YEL-RED; 8P2/8J2 pin 4; 8P5/8J5 pin 4) | ROW 2 (2J7 pin 2, RED-BLK; 8P2/8J2 pin 12; 8P5/8J5 pin 12) | no |
| 8B11 | 8D75 | 11 Left Outlane | COLUMN 2 (2J5 pin 9, YEL-RED; 8P2/8J2 pin 4; 8P5/8J5 pin 4) | ROW 3 (2J7 pin 3, RED-ORN; 8P2/8J2 pin 13; 8P5/8J5 pin 13) | no |
| 8B12 | 8D76 | 12 Right Outlane | COLUMN 2 (2J5 pin 9, YEL-RED; 8P2/8J2 pin 4; 8P5/8J5 pin 4) | ROW 4 (2J7 pin 4, RED-YEL; 8P2/8J2 pin 14; 8P5/8J5 pin 14) | no |
| 8B13 | 8D77 | 13 Right Spinner | COLUMN 2 (2J5 pin 9, YEL-RED; 8P2/8J2 pin 4; 8P5/8J5 pin 4) | ROW 5 (2J7 pin 5, RED-GRN; 8P2/8J2 pin 15; 8P5/8J5 pin 15) | no |
| 8B14 | 8D78 | 14 Ramp Rollunder | COLUMN 2 (2J5 pin 9, YEL-RED; 8P2/8J2 pin 4; 8P5/8J5 pin 4) | ROW 6 (2J7 pin 6, RED-BLU; 8P2/8J2 pin 16; 8P5/8J5 pin 16) | no |
| 8B15 | 8D79 | 15 Right Inside Rollover | COLUMN 2 (2J5 pin 9, YEL-RED; 8P2/8J2 pin 4; 8P5/8J5 pin 4) | ROW 7 (2J7 pin 9, RED-VIO; 8P2/8J2 pin 17; 8P5/8J5 pin 17) | no |
| 8B16 | 8D80 | 16 Left Inside Rollover | COLUMN 2 (2J5 pin 9, YEL-RED; 8P2/8J2 pin 4; 8P5/8J5 pin 4) | ROW 8 (2J7 pin 8, RED-GRY; 8P2/8J2 pin 18; 8P5/8J5 pin 18) | no |
| 8B17 | 8D81 | 17 Bottom Left 3-Bank Lamp | COLUMN 3 (2J5 pin 6, YEL-ORN; 8P2/8J2 pin 5; 8P5/8J5 pin 5) | ROW 1 (2J7 pin 1, RED-BRN; 8P2/8J2 pin 11; 8P5/8J5 pin 11) | no |
| 8B18 | 8D82 | 18 Bottom Right 3-Bank Lamp | COLUMN 3 (2J5 pin 6, YEL-ORN; 8P2/8J2 pin 5; 8P5/8J5 pin 5) | ROW 2 (2J7 pin 2, RED-BLK; 8P2/8J2 pin 12; 8P5/8J5 pin 12) | no |
| 8B19 | 8D83 | 19 Top Left 3-Bank Lamp | COLUMN 3 (2J5 pin 6, YEL-ORN; 8P2/8J2 pin 5; 8P5/8J5 pin 5) | ROW 3 (2J7 pin 3, RED-ORN; 8P2/8J2 pin 13; 8P5/8J5 pin 13) | yes |
| 8B20 | 8D84 | 20 Top Right 3-Bank Lamp | COLUMN 3 (2J5 pin 6, YEL-ORN; 8P2/8J2 pin 5; 8P5/8J5 pin 5) | ROW 4 (2J7 pin 4, RED-YEL; 8P2/8J2 pin 14; 8P5/8J5 pin 14) | yes |
| 8B21 | 8D85 | 21 Center Lock Lamp | COLUMN 3 (2J5 pin 6, YEL-ORN; 8P2/8J2 pin 5; 8P5/8J5 pin 5) | ROW 5 (2J7 pin 5, RED-GRN; 8P2/8J2 pin 15; 8P5/8J5 pin 15) | yes |
| 8B22 | 8D86 | 22 Turnaround Extra Ball When Lit | COLUMN 3 (2J5 pin 6, YEL-ORN; 8P2/8J2 pin 5; 8P5/8J5 pin 5) | ROW 6 (2J7 pin 6, RED-BLU; 8P2/8J2 pin 16; 8P5/8J5 pin 16) | no |
| 8B23 | 8D87 | 23 Turnaround Special | COLUMN 3 (2J5 pin 6, YEL-ORN; 8P2/8J2 pin 5; 8P5/8J5 pin 5) | ROW 7 (2J7 pin 9, RED-VIO; 8P2/8J2 pin 17; 8P5/8J5 pin 17) | no |
| 8B24 | 8D88 | 24 Lower Playfield Eject Hole | COLUMN 3 (2J5 pin 6, YEL-ORN; 8P2/8J2 pin 5; 8P5/8J5 pin 5) | ROW 8 (2J7 pin 8, RED-GRY; 8P2/8J2 pin 18; 8P5/8J5 pin 18) | no |
| 8B25 | 8D89 | 25 Bottom Left 3-Bank, Lower Arrow | COLUMN 4 (2J5 pin 7, YEL-BLK; 8P2/8J2 pin 6; 8P5/8J5 pin 6) | ROW 1 (2J7 pin 1, RED-BRN; 8P2/8J2 pin 11; 8P5/8J5 pin 11) | no |
| 8B26 | 8D90 | 26 Bottom Left 3-Bank, Center Arrow | COLUMN 4 (2J5 pin 7, YEL-BLK; 8P2/8J2 pin 6; 8P5/8J5 pin 6) | ROW 2 (2J7 pin 2, RED-BLK; 8P2/8J2 pin 12; 8P5/8J5 pin 12) | no |
| 8B27 | 8D91 | 27 Bottom Left 3-Bank, Upper Arrow | COLUMN 4 (2J5 pin 7, YEL-BLK; 8P2/8J2 pin 6; 8P5/8J5 pin 6) | ROW 3 (2J7 pin 3, RED-ORN; 8P2/8J2 pin 13; 8P5/8J5 pin 13) | no |
| 8B28 | 8D92 | 28 2X Scoring | COLUMN 4 (2J5 pin 7, YEL-BLK; 8P2/8J2 pin 6; 8P5/8J5 pin 6) | ROW 4 (2J7 pin 4, RED-YEL; 8P2/8J2 pin 14; 8P5/8J5 pin 14) | no |
| 8B29 | 8D93 | 29 Bottom Right 3-Bank, Right Arrow | COLUMN 4 (2J5 pin 7, YEL-BLK; 8P2/8J2 pin 6; 8P5/8J5 pin 6) | ROW 5 (2J7 pin 5, RED-GRN; 8P2/8J2 pin 15; 8P5/8J5 pin 15) | no |
| 8B30 | 8D94 | 30 Bottom Right 3-Bank, Center Arrow | COLUMN 4 (2J5 pin 7, YEL-BLK; 8P2/8J2 pin 6; 8P5/8J5 pin 6) | ROW 6 (2J7 pin 6, RED-BLU; 8P2/8J2 pin 16; 8P5/8J5 pin 16) | no |
| 8B31 | 8D95 | 31 Bottom Right 3-Bank, Left Arrow | COLUMN 4 (2J5 pin 7, YEL-BLK; 8P2/8J2 pin 6; 8P5/8J5 pin 6) | ROW 7 (2J7 pin 9, RED-VIO; 8P2/8J2 pin 17; 8P5/8J5 pin 17) | no |
| 8B32 | 8D96 | 32 3X Scoring | COLUMN 4 (2J5 pin 7, YEL-BLK; 8P2/8J2 pin 6; 8P5/8J5 pin 6) | ROW 8 (2J7 pin 8, RED-GRY; 8P2/8J2 pin 18; 8P5/8J5 pin 18) | no |
| 8B33 | 8D97 | 33 Top Left 3-Bank, Lower Arrow | COLUMN 5 (2J5 pin 3, YEL-GRN; 8P2/8J2 pin 7; 8P5/8J5 pin none (line bypasses 8P5/8J5)) | ROW 1 (2J7 pin 1, RED-BRN; 8P2/8J2 pin 11; 8P5/8J5 pin 11) | yes |
| 8B34 | 8D98 | 34 Top Left 3-Bank, Center Arrow | COLUMN 5 (2J5 pin 3, YEL-GRN; 8P2/8J2 pin 7; 8P5/8J5 pin none (line bypasses 8P5/8J5)) | ROW 2 (2J7 pin 2, RED-BLK; 8P2/8J2 pin 12; 8P5/8J5 pin 12) | yes |
| 8B35 | 8D99 | 35 Top Left 3-Bank, Upper Arrow | COLUMN 5 (2J5 pin 3, YEL-GRN; 8P2/8J2 pin 7; 8P5/8J5 pin none (line bypasses 8P5/8J5)) | ROW 3 (2J7 pin 3, RED-ORN; 8P2/8J2 pin 13; 8P5/8J5 pin 13) | yes |
| 8B36 | 8D100 | 36 Jet Bumper | COLUMN 5 (2J5 pin 3, YEL-GRN; 8P2/8J2 pin 7; 8P5/8J5 pin none (line bypasses 8P5/8J5)) | ROW 4 (2J7 pin 4, RED-YEL; 8P2/8J2 pin 14; 8P5/8J5 pin 14) | yes |
| 8B37 | 8D101 | 37 Top Right 3-Bank, Lower Arrow | COLUMN 5 (2J5 pin 3, YEL-GRN; 8P2/8J2 pin 7; 8P5/8J5 pin none (line bypasses 8P5/8J5)) | ROW 5 (2J7 pin 5, RED-GRN; 8P2/8J2 pin 15; 8P5/8J5 pin 15) | yes |
| 8B38 | 8D102 | 38 Top Right 3-Bank, Center Arrow | COLUMN 5 (2J5 pin 3, YEL-GRN; 8P2/8J2 pin 7; 8P5/8J5 pin none (line bypasses 8P5/8J5)) | ROW 6 (2J7 pin 6, RED-BLU; 8P2/8J2 pin 16; 8P5/8J5 pin 16) | yes |
| 8B39 | 8D103 | 39 Top Right 3-Bank, Upper Arrow | COLUMN 5 (2J5 pin 3, YEL-GRN; 8P2/8J2 pin 7; 8P5/8J5 pin none (line bypasses 8P5/8J5)) | ROW 7 (2J7 pin 9, RED-VIO; 8P2/8J2 pin 17; 8P5/8J5 pin 17) | yes |
| 8B40 | 8D104 | 40 Right Lock Lamp | COLUMN 5 (2J5 pin 3, YEL-GRN; 8P2/8J2 pin 7; 8P5/8J5 pin none (line bypasses 8P5/8J5)) | ROW 8 (2J7 pin 8, RED-GRY; 8P2/8J2 pin 18; 8P5/8J5 pin 18) | yes |
| 8B41 | 8D105 | 41 Left Ramp Rollover Extra Ball When Lit | COLUMN 6 (2J5 pin 5, YEL-BLU; 8P2/8J2 pin 8; 8P5/8J5 pin 8) | ROW 1 (2J7 pin 1, RED-BRN; 8P2/8J2 pin 11; 8P5/8J5 pin 11) | yes |
| 8B42 | 8D106 | 42 Left Lock Lamp | COLUMN 6 (2J5 pin 5, YEL-BLU; 8P2/8J2 pin 8; 8P5/8J5 pin 8) | ROW 2 (2J7 pin 2, RED-BLK; 8P2/8J2 pin 12; 8P5/8J5 pin 12) | yes |
| 8B43 | 8D107 | 43 Not Used | COLUMN 6 | ROW 3 | **no bulb and no diode drawn at this position; neither `8B43` nor `8D107` is printed** |
| 8B44 | 8D108 | 44 Not Used | COLUMN 6 | ROW 4 | **no bulb and no diode drawn at this position; neither `8B44` nor `8D108` is printed** |
| 8B45 | 8D109 | 45 Not Used | COLUMN 6 | ROW 5 | **no bulb and no diode drawn at this position; neither `8B45` nor `8D109` is printed** |
| 8B46 | 8D110 | 46 Not Used | COLUMN 6 | ROW 6 | **no bulb and no diode drawn at this position; neither `8B46` nor `8D110` is printed** |
| 8B47 | 8D111 | 47 Same Player Shoots Again (Playfield) | COLUMN 6 (2J5 pin 5, YEL-BLU; 8P2/8J2 pin 8; 8P5/8J5 pin 8) | ROW 7 (2J7 pin 9, RED-VIO; 8P2/8J2 pin 17; 8P5/8J5 pin 17) | no |
| 8B48 | 8D112 | 48 “1” Bonus | COLUMN 6 (2J5 pin 5, YEL-BLU; 8P2/8J2 pin 8; 8P5/8J5 pin 8) | ROW 8 (2J7 pin 8, RED-GRY; 8P2/8J2 pin 18; 8P5/8J5 pin 18) | no |
| 8B49 | 8D113 | 49 “2” Bonus | COLUMN 7 (2J5 pin 1, YEL-VIO; 8P2/8J2 pin 9; 8P5/8J5 pin 9) | ROW 1 (2J7 pin 1, RED-BRN; 8P2/8J2 pin 11; 8P5/8J5 pin 11) | no |
| 8B50 | 8D114 | 50 “3” Bonus | COLUMN 7 (2J5 pin 1, YEL-VIO; 8P2/8J2 pin 9; 8P5/8J5 pin 9) | ROW 2 (2J7 pin 2, RED-BLK; 8P2/8J2 pin 12; 8P5/8J5 pin 12) | no |
| 8B51 | 8D115 | 51 “4” Bonus | COLUMN 7 (2J5 pin 1, YEL-VIO; 8P2/8J2 pin 9; 8P5/8J5 pin 9) | ROW 3 (2J7 pin 3, RED-ORN; 8P2/8J2 pin 13; 8P5/8J5 pin 13) | no |
| 8B52 | 8D116 | 52 “5” Bonus | COLUMN 7 (2J5 pin 1, YEL-VIO; 8P2/8J2 pin 9; 8P5/8J5 pin 9) | ROW 4 (2J7 pin 4, RED-YEL; 8P2/8J2 pin 14; 8P5/8J5 pin 14) | no |
| 8B53 | 8D117 | 53 “6” Bonus | COLUMN 7 (2J5 pin 1, YEL-VIO; 8P2/8J2 pin 9; 8P5/8J5 pin 9) | ROW 5 (2J7 pin 5, RED-GRN; 8P2/8J2 pin 15; 8P5/8J5 pin 15) | no |
| 8B54 | 8D118 | 54 “7” Bonus | COLUMN 7 (2J5 pin 1, YEL-VIO; 8P2/8J2 pin 9; 8P5/8J5 pin 9) | ROW 6 (2J7 pin 6, RED-BLU; 8P2/8J2 pin 16; 8P5/8J5 pin 16) | no |
| 8B55 | 8D119 | 55 “8” Bonus | COLUMN 7 (2J5 pin 1, YEL-VIO; 8P2/8J2 pin 9; 8P5/8J5 pin 9) | ROW 7 (2J7 pin 9, RED-VIO; 8P2/8J2 pin 17; 8P5/8J5 pin 17) | no |
| 8B56 | 8D120 | 56 “9” Bonus | COLUMN 7 (2J5 pin 1, YEL-VIO; 8P2/8J2 pin 9; 8P5/8J5 pin 9) | ROW 8 (2J7 pin 8, RED-GRY; 8P2/8J2 pin 18; 8P5/8J5 pin 18) | no |
| 8B57 | 8D121 | 57 “10” Bonus | COLUMN 8 (2J5 pin 2, YEL-GRY; 8P2/8J2 pin 10; 8P5/8J5 pin 10) | ROW 1 (2J7 pin 1, RED-BRN; 8P2/8J2 pin 11; 8P5/8J5 pin 11) | no |
| 8B58 | 8D122 | 58 “20” Bonus | COLUMN 8 (2J5 pin 2, YEL-GRY; 8P2/8J2 pin 10; 8P5/8J5 pin 10) | ROW 2 (2J7 pin 2, RED-BLK; 8P2/8J2 pin 12; 8P5/8J5 pin 12) | no |
| 8B59 | 8D123 | 59 “30” Bonus | COLUMN 8 (2J5 pin 2, YEL-GRY; 8P2/8J2 pin 10; 8P5/8J5 pin 10) | ROW 3 (2J7 pin 3, RED-ORN; 8P2/8J2 pin 13; 8P5/8J5 pin 13) | no |
| 8B60 | 8D124 | 60 “40” Bonus | COLUMN 8 (2J5 pin 2, YEL-GRY; 8P2/8J2 pin 10; 8P5/8J5 pin 10) | ROW 4 (2J7 pin 4, RED-YEL; 8P2/8J2 pin 14; 8P5/8J5 pin 14) | no |
| 8B61 | 8D125 | 61 2x | COLUMN 8 (2J5 pin 2, YEL-GRY; 8P2/8J2 pin 10; 8P5/8J5 pin 10) | ROW 5 (2J7 pin 5, RED-GRN; 8P2/8J2 pin 15; 8P5/8J5 pin 15) | no |
| 8B62 | 8D126 | 62 3x | COLUMN 8 (2J5 pin 2, YEL-GRY; 8P2/8J2 pin 10; 8P5/8J5 pin 10) | ROW 6 (2J7 pin 6, RED-BLU; 8P2/8J2 pin 16; 8P5/8J5 pin 16) | no |
| 8B63 | 8D127 | 63 4x | COLUMN 8 (2J5 pin 2, YEL-GRY; 8P2/8J2 pin 10; 8P5/8J5 pin 10) | ROW 7 (2J7 pin 9, RED-VIO; 8P2/8J2 pin 17; 8P5/8J5 pin 17) | no |
| 8B64 | 8D128 | 64 5x | COLUMN 8 (2J5 pin 2, YEL-GRY; 8P2/8J2 pin 10; 8P5/8J5 pin 10) | ROW 8 (2J7 pin 8, RED-GRY; 8P2/8J2 pin 18; 8P5/8J5 pin 18) | no |

## Printed bulb list (right edge of sheet), verbatim
Headed `Bulb` / `No.` and `Function`. Entries `01`-`64` (the same legends are repeated in the table above for 09-64):
01 Same Player Shoots Again (Backbox); 02 Ball in Play; 03 Tilt; 04 Game Over; 05 Match; 06 High Score to Date;
07 Credits (Playfield); 08 Bonus Ball Timer; 09 Right *Magna-Save*; 10 Left *Magna-Save*; 11 Left Outlane;
12 Right Outlane; 13 Right Spinner; 14 Ramp Rollunder; 15 Right Inside Rollover; 16 Left Inside Rollover;
17 Bottom Left 3-Bank Lamp; 18 Bottom Right 3-Bank Lamp; 19 Top Left 3-Bank Lamp; 20 Top Right 3-Bank Lamp;
21 Center Lock Lamp; 22 Turnaround Extra Ball When Lit; 23 Turnaround Special; 24 Lower Playfield Eject Hole;
25 Bottom Left 3-Bank, Lower Arrow; 26 Bottom Left 3-Bank, Center Arrow; 27 Bottom Left 3-Bank, Upper Arrow; 28 2X Scoring;
29 Bottom Right 3-Bank, Right Arrow; 30 Bottom Right 3-Bank, Center Arrow; 31 Bottom Right 3-Bank, Left Arrow; 32 3X Scoring;
33 Top Left 3-Bank, Lower Arrow; 34 Top Left 3-Bank, Center Arrow; 35 Top Left 3-Bank, Upper Arrow; 36 Jet Bumper;
37 Top Right 3-Bank, Lower Arrow; 38 Top Right 3-Bank, Center Arrow; 39 Top Right 3-Bank, Upper Arrow; 40 Right Lock Lamp;
41 Left Ramp Rollover Extra Ball When Lit; 42 Left Lock Lamp; 43 Not Used; 44 Not Used; 45 Not Used; 46 Not Used;
47 Same Player Shoots Again (Playfield); 48 "1" Bonus; 49 "2" Bonus; 50 "3" Bonus; 51 "4" Bonus; 52 "5" Bonus;
53 "6" Bonus; 54 "7" Bonus; 55 "8" Bonus; 56 "9" Bonus; 57 "10" Bonus; 58 "20" Bonus; 59 "30" Bonus; 60 "40" Bonus;
61 2x; 62 3x; 63 4x; 64 5x. (Quotation marks printed as curly double quotes; no other notes in the list.)

## Observations
- Positions with no bulb: 8B43, 8B44, 8B45, 8B46 are `Not Used` in the printed list. In the matrix the cells in the COLUMN 6
  group at rows 3, 4, 5, 6 (between 8B42 and 8B47) are empty: no lamp symbol, no diode, no `8B43`-`8B46` and no
  `8D107`-`8D110` printed. COLUMN 6's vertical wire runs down through the empty cells to 8B47 and 8B48. The row wires for rows
  3-6 continue through those empty cells.
- `COLUMN 1` (8J2 pin 3, YEL-BRN on 2P5 pin 8; 8P5/8J5 pin 3) is printed `NC` on the 8J5 side; no bulb is drawn on it.
- Bulb numbers 01-08 are listed in the legend but not drawn on this sheet.
- The grey-shading key says shaded bulbs are on the upper playfield and "connections are not routed through 8P5/8J5".
  The shaded cells are 8B19-8B21 (COLUMN 3 group), 8B33-8B40 (all of COLUMN 5) and 8B41-8B42 (COLUMN 6 group). COLUMN 5 is
  the only column drawn without passing through 8P5/8J5. COLUMN 3 and COLUMN 6 are drawn through 8P5/8J5 pins 5 and 8
  respectively (shared with their unshaded bulbs), and every row wire (ROW 1-8) is drawn through 8P5/8J5 pins 11-18, so for
  shaded bulbs the drawing shows the row wires and, for 8B19-8B21 and 8B41-8B42, the column wires passing through 8P5/8J5 even
  though the key says their connections are not routed through it. Recorded as drawn.
- Every bulb is drawn once (no lamp is drawn as two bulbs in parallel, and no bulb designator is printed twice). The six
  general-illumination lamps carry no designators.
- Column order versus bulb numbering: COLUMN 2 carries 8B9-8B16, COLUMN 3 carries 8B17-8B24, ..., COLUMN 8 carries
  8B57-8B64 (bulb number = 8 x (column - 2) + 9 + (row - 1)).
- The diode designators are 8D73-8D128 (diode number = bulb number + 64) except that 8D107-8D110 are not printed.
- General illumination wire colours `YEL` and `YEL-WHT` are drawn as dotted lines that end at the 8P8 arrow stubs; `VIO` and
  `WHT` are solid and continue to 8P2 pins 1 and 2.

## Illegible / uncertain items
None. The 8D83 label inside the shaded cell (bulb 8B19) is partly obscured by the shading but reads `8D83`
(consistent with the other seven diodes in that column, 8D81-8D88).
