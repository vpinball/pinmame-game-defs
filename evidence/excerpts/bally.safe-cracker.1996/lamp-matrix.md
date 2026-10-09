# Safe Cracker — Lamp Matrix (wiring)

Transcribed from `Bally_1996_Safe_Cracker_Manual.pdf`, PDF page 118, printed page `2-46`: the `LAMP MATRIX` table
(title line, column headers, row headers, the 64 cells and the footnote). The lower part of the same PDF page is the
first `LAMP LOCATIONS` parts list (items 11-68), transcribed in `lamp-locations.md`. The Section 3 reprint on PDF page
128 (printed `3-4`) was compared cell by cell; a third printing on PDF page 157 (printed folio not visible) was also
compared (see below). Read from the rendered page (300 dpi scan), not from the OCR text.

The title line prints `LAMP MATRIX`, then at the right the labels `Yellow (B+)`, a lamp (bulb) symbol drawn as a loop in
the line, and `Red`. A diode symbol (arrowhead and bar) is printed in the line between the lamp and `Red`.

## Matrix drive columns

| Column | Wire (as printed) | Connector-pin | Drive transistor |
| --- | --- | --- | --- |
| 1 | Yellow-Brown | J121-1 | Q96 |
| 2 | Yellow-Red | J121-2 | Q100 |
| 3 | Yellow-Orange | J121-3 | Q95 |
| 4 | Yellow-Black | J121-4 | Q99 |
| 5 | Yellow-Green | J121-5 | Q94 |
| 6 | Yellow-Blue | J121-6 | Q98 |
| 7 | Yellow-Violet | J121-7 | Q93 |
| 8 | Yellow-Gray | J121-9 | Q97 |

The top-left corner cell is divided diagonally and prints `Column` (upper right) and `Row` (lower left). Each column
header prints the column number (bold), the wire name on two lines (`Yellow-` over `Brown`, bold), the connector-pin
and the transistor on separate lines. Column 8's connector pin is `J121-9` (there is no `J121-8` column).

## Matrix return rows

| Row | Wire (as printed) | Connector-pin | Return transistor |
| --- | --- | --- | --- |
| 1 | Red-Brown | J125-1 | Q104 |
| 2 | Red-Black | J125-2 | Q108 |
| 3 | Red-Orange | J125-4 | Q103 |
| 4 | Red-Yellow | J125-5 | Q107 |
| 5 | Red-Green | J125-6 | Q102 |
| 6 | Red-Blue | J125-7 | Q106 |
| 7 | Red-Violet | J125-8 | Q101 |
| 8 | Red-Gray | J125-9 | Q105 |

The row header prints the row number at the left, the wire name on two lines (`Red-` over `Brown`, bold) and the
connector-pin and transistor on one line (`J125-1 Q104`). The row pins skip `J125-3` (row 2 is `J125-2`, row 3 is
`J125-4`).

## Matrix cells

Each cell prints its description (multi-line text, joined here by single spaces) and a small two-digit lamp number in
its bottom-right corner, column digit first, row digit second. Double quotation marks are printed as typographic
quotes and are shown here as straight quotes. No cell is shaded and no cell is blank; the only legend is the footnote
below.

| Row | Col 1 | Col 2 | Col 3 | Col 4 |
| --- | --- | --- | --- | --- |
| 1 | 11 LITE DEPOSIT | 21 CENTER TIMER "15" | 31 ARMOR CAR CELLAR | 41 BONUS 5X + OUTLANE |
| 2 | 12 CENTER TIMER "10" | 22 CENTER TIMER "20" | 32 ARMOR CAR ROOF | 42 BONUS 5X |
| 3 | 13 DISABLE COMPUTER | 23 CENTER TIMER "25" | 33 ARMOR CAR MAIN | 43 BONUS 4X |
| 4 | 14 CENTER TIMER "5" | 24 CENTER TIMER "30" | 34 BONUS 2X | 44 BONUS 3X |
| 5 | 15 CENTER TIMER "0" | 25 CENTER TIMER "35" | 35 (A)LARM STANDUP | 45 RAMP LOCK |
| 6 | 16 LITE LOCK | 26 CALL GUARD | 36 ATM CARD | 46 AL(A)RM STANDUP |
| 7 | 17 CENTER TIMER "55" | 27 CENTER TIMER "45" | 37 A(L)ARM STANDUP | 47 ALA(R)M STANDUP |
| 8 | 18 CENTER TIMER "50" | 28 CENTER TIMER "40" | 38 RAMP JACKPOT | 48 ALAR(M) STANDUP |

| Row | Col 5 | Col 6 | Col 7 | Col 8 |
| --- | --- | --- | --- | --- |
| 1 | 51 WHEEL ARROW | 61 TOP RIGHT 3-BANK TOP | 71 BOTTOM R. 3-BANK TOP | 81 TOP JET (YELLOW) |
| 2 | 52 LITE OUTLANES | 62 TOP RIGHT 3-BANK MIDDLE | 72 BOTTOM R. 3-BANK MIDDLE | 82 LEFT JET (CLEAR) |
| 3 | 53 INVISIBLE CODE | 63 TOP RIGHT 3-BANK BOTTOM | 73 BOTTOM R. 3-BANK BOTTOM | 83 RIGHT JET (RED) |
| 4 | 54 EXPLOSIVES | 64 TOP LEFT 3-BANK TOP | 74 BOTTOM L. 3-BANK TOP | 84 BANK LEFT |
| 5 | 55 NOTE TO TELLER | 65 TOP LEFT 3-BANK MIDDLE | 75 BOTTOM R. 3-BANK MIDDLE | 85 BANK RIGHT |
| 6 | 56 TOP LEFT LANE | 66 TOP LEFT 3-BANK BOTTOM | 76 BOTTOM R. 3-BANK BOTTOM | 86 VARI BREAK IN |
| 7 | 57 TOP MIDDLE LANE | 67 RIGHT "EXTRA TIME" | 77 LEFT RETURN | 87 ROOF BREAK IN |
| 8 | 58 TOP RIGHT LANE | 68 RIGHT RETURN | 78 LEFT "EXTRA TIME" | 88 START BUTTON |

Notes on the cell text:

- Cell 54 `EXPLOSIVES` is printed in a smaller type size than the other cell texts (it is on one line).
- Cell 74 prints `BOTTOM L.` (left); cells 71, 72, 73, 75 and 76 print `BOTTOM R.` (right). The matching Lamp
  Locations rows for items 74, 75, 76 are all `Bottom Left 3-Bank Top / Middle / Bottom`; see Observations.
- Cell 31 prints `ARMOR CAR CELLAR`, 32 `ARMOR CAR ROOF`, 33 `ARMOR CAR MAIN` (three lines each: `ARMOR` / `CAR` / word).
- Parenthesised letters in `(A)LARM`, `A(L)ARM`, `AL(A)RM`, `ALA(R)M`, `ALAR(M)` (cells 35, 37, 46, 47, 48) are printed
  exactly so; together they spell ALARM.
- The digit printed in the corner of cell 81 is slightly blotted on the scan (it reads as `81` at 300 dpi crop; at
  low resolution it looks like `61`). Its position (column 8, row 1) fixes it as 81.
- The Center Timer lamps are `"0"` (15), `"5"` (14), `"10"` (12), `"15"` (21), `"20"` (22), `"25"` (23), `"30"` (24),
  `"35"` (25), `"40"` (28), `"45"` (27), `"50"` (18), `"55"` (17); the numbering is not in time order.
- Cells 61-63 are `TOP RIGHT`, 64-66 are `TOP LEFT`.

## Footnote

`J1XX = Power Driver Board` (printed below the table, left). No other legend, asterisk or shading is printed on this
table.

## Observations

- Within column 7 the matrix prints `BOTTOM R.` for cells 75 and 76 while the Lamp Locations list on the same PDF page
  (items 75, 76) prints `Bottom Left 3-Bank Middle` and `Bottom Left 3-Bank Bottom`, and the matrix prints `BOTTOM L.`
  only for cell 74. All three printings of the matrix (PDF pages 118, 128, 157) agree with one another, so this is
  the manual's own printed disagreement, not a transcription difference.
  (Items 71-73 are `Bottom Right 3-Bank ...` in the list and `BOTTOM R.` in the matrix, consistent.)
- The matrix cell labels otherwise agree with the Lamp Locations descriptions (`lamp-locations.md`) item by item,
  apart from capitalization and punctuation.

## Comparison with the reprint (Section 3, PDF page 128, printed page `3-4`)

The Section 3 reprint prints the same `LAMP MATRIX` (title line with `Yellow (B+)`, lamp symbol, diode and `Red`; the
diagonal corner cell; footnote `J1XX = Power Driver Board`) followed by a `LAMP MATRIX CIRCUIT` drawing and text. Every
column header (wire, connector-pin, transistor), every row header and all 64 cells (label and corner number) were
compared with the PDF page 118 reading above: no differences found. The reprint's printed folio is `3-4`.

The `LAMP MATRIX CIRCUIT` drawing on the reprint page (outside this table, summarised for completeness) prints a
`Column (example)` circuit (`J102`, `LS240`, `LS374` on the `POWER DRIVER BOARD`, `ULN-2803` (point `A`), `560`, `1.2K`
to `+18V`, `TIP107` (point `B`), `J1XX` `Yellow-XXX` to a lamp and a diode on the `PLAYFIELD`) and a `Row (example)`
circuit (`J1XX` `Red-XXX`, `LS74` with `D`, `CLK`, `Q`, `Q-bar` (point `F`), `G`, `1K`, `TIP102` (point `E`), `.22`, `2.2K`,
`.1mf`, `1.4V ref`, `LM339` (point `C`, `D`), `10K` to `VCC`) with the truth tables `COLUMN | A | B`: `H L OFF`, `L H ON`
and `ROW | C D E F G`: `NORMAL H L H L H OFF`, `OPERATION H L L H L ON`. The text beneath reads (printed typos kept):
`The microprocessor sends a signal to the column circuit causing  the output of the UNL-2803 to toggle. When point "A" drops low, the TIP107 transistor conducts and point "B" changes to a high state. At the same time, the microprocessor drives the input of the 74LS74 low, causing a high at output "F". A high state at the base of the TIP102 causes the transistor to conducts, bringing the row circuit to ground and turning the lamp on. The microprocessor changes the input of the 74LS74 to a high state to turn the lamp off. In overcurrent conditions, the lamp is shut off through the comparator. If the voltage at the negative input of the LM339 rises above 1.4V, the output changes to a low, which is fed back to the 74LS74 and shuts the circuit off.`
(printed typos `UNL-2803` in the first sentence and `to conducts` are as shown; the circuit drawing itself prints `ULN-2803`.)

## Third printing (PDF page 157)

PDF page 157 (no folio visible) prints the same `LAMP MATRIX` a third time, above a third printing of the `SWITCH MATRIX`. All
headers and 64 cells compared: no differences found. It is not an auxiliary-board matrix: the 48 backbox lamps L1-L48 of
the 48 Lamp & Driver P.C.B. A-20909 have no matrix page (see `lamp-locations.md` and `aux-lamp-board.md`).

## Reading uncertainties

None in the headers or cell text. The only low-contrast glyph is the corner number of cell 81 (see notes); its value is
fixed by position.
