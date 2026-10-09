# Diner — Lamp-Matrix Table (printed page 76)

Source: `Williams_1990_Diner_Operations_Manual_June_1990_includes_schematics_OCR_searchable.pdf` (106
pages, SHA-256 `da75ffb79e6d6b8d1b332ce65f93ee1486a5a7ff8d9060878f07a91438b573aa`), PDF page 80 (printed
"DINER 76", the page footer prints `DINER 76`). Read from the rendered 150 dpi page image, cropped and
enlarged in strips; the OCR text layer was not trusted. The page carries the lamp-matrix wiring drawing at
the top and the "DINER Lamp-Matrix Table" below it. Every cell is transcribed. In each table cell the lamp
number is printed at the lower right and the name above it, with any location text in parentheses under
the name. A circled "2" printed in a cell is written `(2)` here; the legend line below the table explains
it as "= Multiple Lamps". The table prints no item identifiers or shaded cells.

The page prints no introductory paragraph.

## Matrix wiring drawing (top of page)

Connector label `1P7 - 2J3` (column lines). Printed, from top to bottom, as `1P7 pin | 2J3 pin | wire |
column label`:

| 1P7 pin | 2J3 pin | Wire | Label |
| --- | --- | --- | --- |
| 9 | 1 | YEL-GRY | Column 8 |
| 8 | 2 | YEL-VIO | Column 7 |
| 7 | 3 | YEL-BLU | Column 6 |
| 6 | 4 | YEL-GRN | Column 5 |
| 4 | 5 | YEL-BLK | Column 4 |
| 3 | 6 | YEL-ORN | Column 3 |
| 2 | 7 | YEL-RED | Column 2 |
| 1 | 8 | YEL-BRN | Column 1 |

(No 1P7 pin 5 is printed in the drawing.)

Connector label `1P6 - 2J3` (row lines). Printed, from top to bottom:

| 1P6 pin | 2J3 pin | Wire | Label |
| --- | --- | --- | --- |
| 1 | 18 | RED-BRN | Row 1 |
| 2 | 17 | RED-BLK | Row 2 |
| 3 | 16 | RED-ORN | Row 3 |
| 5 | 15 | RED-YEL | Row 4 |
| 6 | 14 | RED-GRN | Row 5 |
| 7 | 13 | RED-BLU | Row 6 |
| 8 | 12 | RED-VIO | Row 7 |
| 9 | 11 | RED-GRY | Row 8 |

(No 1P6 pin 4 is printed in the drawing.)

The drawing is an 8 x 8 grid of crossing lines. Each crossing carries a slanted mark labelled with the
lamp number printed as two digits: column 1 holds `01` to `08` (top to bottom, rows 1 to 8), column 2 `09`
to `16`, column 3 `17` to `24`, column 4 `25` to `32`, column 5 `33` to `40`, column 6 `41` to `48`,
column 7 `49` to `56`, column 8 `57` to `64`. At the right edge a small symbol, labelled `Column` (top) and
`Row` (bottom), shows a lamp symbol in series with a diode between the column line and the row line.

## DINER Lamp-Matrix Table

Column headers (each prints the column number and the driver transistor on the top line, then the column
wire, then the connector pin): 1 Q66 YEL-BRN 1J7-1; 2 Q64 YEL-RED 1J7-2; 3 Q62 YEL-ORN 1J7-3; 4 Q60
YEL-BLK 1J7-4; 5 Q58 YEL-GRN 1J7-6; 6 Q56 YEL-BLU 1J7-7; 7 Q54 YEL-VIO 1J7-8; 8 Q52 YEL-GRY 1J7-9.
(Column 5 prints 1J7-6; no column prints 1J7-5.) The top-left header cell is split diagonally and prints
`COLUMN` (upper right) and `ROW` (lower left).

Row headers (the driver transistor at the upper left, the row number below it, then the row wire printed
on two lines with a hyphen after the first part, then the connector pin): Q80 row 1 RED-BRN 1J6-1; Q81
row 2 RED-BLK 1J6-2; Q82 row 3 RED-ORN 1J6-3; Q83 row 4 RED-YEL 1J6-5; Q84 row 5 RED-GRN 1J6-6; Q85 row
6 RED-BLU 1J6-7; Q86 row 7 RED-VIO 1J6-8; Q87 row 8 RED-GRY 1J6-9. (Row 4 prints 1J6-5; no row prints
1J6-4.)

Cells are written as printed, name first, then any parenthetical, then the printed lamp number. A
parenthetical or a second text line printed under the name is written after it. `(2)` is the circled
"2" printed to the upper right of the cell text.

| Row | Column 1 | Column 2 | Column 3 | Column 4 | Column 5 | Column 6 | Column 7 | Column 8 |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1 (Q80) | 20K (C Regstr) 1 | Serve Again 9 | D (in DINER) 17 | Jukebox 1 25 | Haji 33 | 100K Grill BONUS 41 | 1 o'clock Dine Time 49 | 9 o'clock Dine Time 57 |
| 2 (Q81) | 40K (C Regstr) 2 | Ramp Scores 500K (L Ramp) 10 | I (in DINER) 18 | Jukebox 2 26 | Babs 34 | 250K Grill BONUS 42 | 2 o'clock Dine Time 50 | 10 o'clock Dine Time 58 |
| 3 (Q82) | 60K (C Regstr) 3 | Ramp Scores 500K (R Ramp) 11 | N (in DINER) 19 | Jukebox 3 27 | Boris 35 | 500K Grill BONUS 43 | 3 o'clock Dine Time 51 | 11 o'clock Dine Time 59 |
| 4 (Q83) | 80K (C Regstr) 4 | LOCK (L Ramp) 12 | E (in DINER) 20 | Jukebox 4 28 | Pepe 36 | 1 Million Grill BONUS 44 | 4 o'clock Dine Time 52 | 12 o'clock Dine Time 60 |
| 5 (Q84) | 100K (C Regstr) 5 | Release (Upr Right) 13 | R (in DINER) 21 | Jukebox 5 29 | Buck 37 | Extra Ball Grill BONUS 45 | 5 o'clock Dine Time 53 | Top 5 Hits w/Lit 61 |
| 6 (Q85) | Adv DINE TIME (L Return Lane) 6 | RUSH 1 (Upr Right) 14 | E (2) (Top Lane) 22 | Hot Dog (C Dr Tgt) 30 | Root Beer (L Dr Tgt) 38 | Spot Food (L) 46 | 6 o'clock Dine Time 54 | Today's Special 62 |
| 7 (Q86) | Adv DINE TIME (R Return Lane) 7 | RUSH 2 (Lwr Right) 15 | A (2) (Top Lane) 23 | Burger (C Dr Tgt) 31 | Fries (L Dr Tgt) 39 | Cup Scores 10X Diner Letter 47 | 7 o'clock Dine Time 55 | Dine Time Collect 63 |
| 8 (Q87) | Extra Ball (Right Outlane) 8 | Spinner 16 | T (2) (Top Lane) 24 | Chili (C Dr Tgt) 32 | Iced Tea (L Dr Tgt) 40 | Extra Ball (Left Outlane) 48 | 8 o'clock Dine Time 56 | Spot Food (R) 64 |

No cell in this table is blank. Legend line printed under the table: "BR = Bottom right;  BL = Bottom Left   (circle) = Multiple Lamps"
(an empty circle symbol is printed before "= Multiple Lamps"). Note the capitalization as printed:
"Bottom right" (lower-case r) and "Bottom Left".

## Comparison with the copy on PDF page 35 (printed "DINER 31")

PDF page 35 (printed `DINER 31`, "TEST/DIAGNOSTIC PROCEDURES (Continued)", "LAMP TESTS", "1. All Lamps.",
"2. Single Lamps.") prints the same "DINER Lamp-Matrix Table" with the same legend line. Its introductory
text says "To locate the wiring associated with a particular feature lamp, refer to the Lamp-Matrix Table.
CPU Board connections at jacks 1J6 (columns) and 1J7 (rows) are also listed in the table." (The text names
1J6 as columns and 1J7 as rows, whereas the table headers print 1J7 on the columns and 1J6 on the rows; this
is a difference inside the page 35 prose, not in the table.) The copy has no wiring drawing. Read cell by
cell from enlarged crops: all 64 cell names, parentheticals, circled-2 markers and numbers, all eight
column headers (number, transistor, wire, pin), all eight row headers (transistor, number, wire, pin) and
the legend line agree with the page 80 table. There is no difference in any printed word or digit. Print
differences only: slightly different line breaks and spacing (for example "(Top Lane)22" and "Grill
BONUS41" touch their numbers in both copies), and a faint smudge beside "2 o'clock" in cell 50.

## Comparison with the copy on PDF page 105 (no folio printed)

PDF page 105 prints the Lamp-Matrix Table above a Switch-Matrix Table, with no page text or folio. Read
the same way, the Lamp-Matrix Table agrees with the page 80 table in every cell, circled-2 marker, header
and the legend line, with no difference in any printed word or digit. Print differences only: the page is
set smaller, the opening parenthesis of "(L Return Lane)" is clipped by the cell border, and a small mark
appears beside "4" in cell 28.

The OCR layer was not used for any cell.

Normalization: circled "2" is written `(2)`; cell text printed on several lines is joined with single
spaces; the two-line wire `RED-` / `BRN` is written `RED-BRN`; the row header is written as row number
with the printed Q-number in parentheses.

Uncertain cells:
- Row 6 and row 7, column 1 (lamps 6 and 7): "Adv DINE TIME" runs into the right cell border so that the
  final "E" is partly clipped on all three copies. Read as "TIME"; no other reading is plausible but the
  last letter is not fully formed.
- Row 4 header: pin printed `1J6-5`; row 5 `1J6-6`. These are read as printed and match the wiring drawing
  (row 4 on 1P6 pin 5, row 5 on pin 6).
- The circled marker in column 3 rows 6 to 8 is read as `2` in all three copies.
