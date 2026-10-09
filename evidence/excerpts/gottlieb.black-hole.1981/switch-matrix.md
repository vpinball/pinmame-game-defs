# Black Hole — Upper and lower playfield switch matrix (printed page 43)

Source: the Scribd copy of the Gottlieb *Black Hole Instruction Manual* (document 223467608), viewer page 45 (printed
page 43), drawing E-21340 "UPPER AND LOWER PLAYFIELD SWITCH MATRIX, SYSTEM 80, GAME #668", dated 24 JUNE 1981. Read
from the 904 x 1160 page image, enlarged in three crops; every cell below was read from the drawing.

Layout of the sheet: eight strobes (rows) enter from the A1 control board on P/O A1J6 pins 1-8, and seven returns
(columns) go back to A1 on P/O A1J6 pins 10-16. Every cell holds a diode (note 1: "ALL DIODES ARE 1N270"), the switch
name, the wire colour in a box on the diode side, and the switch number printed as "SW.nn". Note 2 reads "RETURN 7 NOT
USED." Strobes 4-7 and returns 0-3 run through P/O A9J7 / A9P7 to a dashed block labelled "LOCATED ON LOWER PLAYFIELD".
Wire colours are three-digit codes (0 black, 1 brown, 2 red, 3 orange, 4 yellow, 5 green, 6 blue, 7 purple, 8 slate,
9 white, from the colour-code box on the sheet).

## Strobe and return lines

| Line | Connector pin | Wire |
| --- | --- | --- |
| Strobe 0 | A1J6-1 | 400 |
| Strobe 1 | A1J6-2 | 411 |
| Strobe 2 | A1J6-3 | 422 |
| Strobe 3 | A1J6-4 | 433 |
| Strobe 4 | A1J6-5, A9J7/A9P7-1 | 444 |
| Strobe 5 | A1J6-6, A9J7/A9P7-2 | 455 |
| Strobe 6 | A1J6-7, A9J7/A9P7-3 | 466 |
| Strobe 7 | A1J6-8, A9J7/A9P7-4 | 477 |
| Return 0 | A1J6-10 (lower playfield: A9J7/A9P7-5) | 600 |
| Return 1 | A1J6-11 (lower playfield: A9J7/A9P7-6) | 611 |
| Return 2 | A1J6-12 (lower playfield: A9J7/A9P7-7); A9J2/A9P2-6 to the right drop bank | 622 |
| Return 3 | A1J6-13 (lower playfield: A9J7/A9P7-8); A9J3/A9P3-7 to the left drop bank | 633 |
| Return 4 | A1J6-14; A9J3/A9P3-8 to the left drop bank | 644 |
| Return 5 | A1J6-15 | 655 |
| Return 6 | A1J6-16 | 666 |

## Cells

| SW | Strobe | Return | Name as printed | Wire | Drop-target connector pin |
| --- | --- | --- | --- | --- | --- |
| 00 | 0 | 0 | TOP #1 ROLLOVER | 111 | |
| 01 | 0 | 1 | #1 SPOT TARGET | 344 | |
| 02 | 0 | 2 | RIGHT #1 DROP TARGET "H" | 033 | A9J2/A9P2 1 |
| 03 | 0 | 3 | LEFT #1 DROP TARGET "B" | 100 | A9J3/A9P3 1 |
| 04 | 0 | 4 | LEFT #4 DROP TARGET "C" | 166 | A9J3/A9P3 4 |
| 05 | 0 | 5 | BALL KICKER HOLE SWITCH | 800 | |
| 06 | 0 | 6 | POP BUMPERS (4) | 855 | |
| 10 | 1 | 0 | TOP #2 ROLLOVER | 133 | |
| 11 | 1 | 1 | #2 SPOT TARGET | 355 | |
| 12 | 1 | 2 | RIGHT #2 DROP TARGET "O" | 055 | A9J2/A9P2 2 |
| 13 | 1 | 3 | LEFT #2 DROP TARGET "L" | 122 | A9J3/A9P3 2 |
| 14 | 1 | 4 | LEFT #5 DROP TARGET "K" | 177 | A9J3/A9P3 5 |
| 15 | 1 | 5 | OUTHOLE | 833 | |
| 16 | 1 | 6 | LEFT SPINNING TARGET | 811 | |
| 20 | 2 | 0 | TOP #3 ROLLOVER | 144 | |
| 21 | 2 | 1 | #3 SPOT TARGET | 366 | |
| 22 | 2 | 2 | RIGHT #3 DROP TARGET "L" | 066 | A9J2/A9P2 3 |
| 23 | 2 | 3 | LEFT #3 DROP TARGET "A" | 155 | A9J3/A9P3 3 |
| 24 | 2 | 4 | TOP LANE ROLLUNDER SWITCH | 844 | |
| 25 | 2 | 5 | 3RD POSITION BALL RETURN (TROUGH) | 333 | |
| 26 | 2 | 6 | TILT SWITCH (PLAYBOARD) | 011 | |
| 30 | 3 | 0 | RIGHT SIDE ROLLOVER | 300 | |
| 31 | 3 | 1 | #4 SPOT TARGET | 377 | |
| 32 | 3 | 2 | RIGHT #4 DROP TARGET "E" | 077 | A9J2/A9P2 4 |
| 33 | 3 | 3 | BLACK HOLE ROLLOVER | 822 | |
| 34 | 3 | 4 | 10 POINT SWITCHES (5) | 044 | |
| 35 | 3 | 5 | RIGHT RETURN ROLLOVER | 711 | |
| (36) | 3 | 6 | blank: no cell is drawn | | |
| 40 | 4 | 0 | LEFT #1 DROP TARGET | 700 | (lower playfield) |
| 41 | 4 | 1 | RIGHT #1 DROP TARGET | 744 | (lower playfield) |
| 42 | 4 | 2 | HOLE KICKER SWITCH | 533 | (lower playfield) |
| 43 | 4 | 3 | BALL TUBE KICKER SWITCH | 844 | (lower playfield) |
| 50 | 5 | 0 | LEFT #2 DROP TARGET | 711 | (lower playfield) |
| 51 | 5 | 1 | RIGHT #2 DROP TARGET | 755 | (lower playfield) |
| 52 | 5 | 2 | ROLLUNDER GATE | 566 | (lower playfield) |
| 53 | 5 | 3 | TRACK SWITCH | 855 | (lower playfield) |
| 60 | 6 | 0 | LEFT #3 DROP TARGET | 722 | (lower playfield) |
| 61 | 6 | 1 | RIGHT #3 DROP TARGET | 766 | (lower playfield) |
| 62 | 6 | 2 | RETURN ROLLOVER | 577 | (lower playfield) |
| (63) | 6 | 3 | blank: no cell is drawn | | |
| 70 | 7 | 0 | LEFT #4 DROP TARGET | 733 | (lower playfield) |
| 71 | 7 | 1 | LOWER LEVEL POP BUMPERS (2) | 777 | (lower playfield) |
| 72 | 7 | 2 | 10 POINT SWITCHES AND KICKING TARGET | 288 | (lower playfield) |
| (73) | 7 | 3 | blank: no cell is drawn | | |

No cell is drawn for strobes 4-7 on returns 4-6 (44-46, 54-56, 64-66, 74-76), and return 7 is "NOT USED" on this
sheet, so 07, 17, 27, 37, 47, 57, 67 and 77 do not appear here at all. The return-6 column has cells only on strobes 0-2.

Two wire colours repeat on the sheet as printed: 711 on both SW.35 and SW.50, and 844 on both SW.24 and SW.43; the
cells are on different playfields and connectors, so they are transcribed as printed. A handwritten "ECG 285 =" beside
the tilt-switch cell is an owner's annotation and not part of the drawing.
