# NBA Fastbreak — Lamp Matrix (wiring)

Transcribed from `Bally_1997_NBA_Fastbreak_Operations_Manual_May_1997_Final_with_schematics.pdf` (document
16-50053.1-101, May 1997), PDF page 67, right half of the 2-up spread, printed page `2-49`: the `LAMP MATRIX` table
with its column and row headers, the 64 cells and the footnote. The left half of the same PDF page is the Switch
Matrix (`switch-matrix.md`). The same table in the March 1997 edition
(`Bally_1997_NBA_Fastbreak_Operations_Manual_Final_no_schematics.pdf`, PDF page 125) was read as well. Read from
the rendered page (300 dpi scan), not from the OCR text.

The title line prints `LAMP MATRIX`, then at the right the labels `Yellow (B+)`, a lamp (bulb) symbol drawn as a
loop in the line, and `Red`. On this `2-49` page the line after the lamp ends in a short dash and no diode symbol is
printed before `Red`; the March scan and the Section 3 reprint on PDF page 71 (`3-4`) print a diode (arrowhead and bar)
between the lamp and `Red`.

## Matrix drive columns

| Column | Wire | Connector-pin | Drive transistor |
| --- | --- | --- | --- |
| 1 | Yellow-Brown | J121-1 | Q96 |
| 2 | Yellow-Red | J121-2 | Q100 |
| 3 | Yellow-Orange | J121-3 | Q95 |
| 4 | Yellow-Black | J121-4 | Q99 |
| 5 | Yellow-Green | J121-5 | Q94 |
| 6 | Yellow-Blue | J121-6 | Q98 |
| 7 | Yellow-Violet | J121-7 | Q93 |
| 8 | Yellow-Gray | J121-9 | Q97 |

The top-left corner cell is divided diagonally and prints `Column` and `Row`. Column 8's connector pin is `J121-9`
(there is no `J121-8` column). Wire names are printed on two lines (`Yellow-` over `Brown`); column 5's `Yellow-Green`
is printed on a single line.

## Matrix return rows

| Row | Wire | Connector-pin | Return transistor |
| --- | --- | --- | --- |
| 1 | Red-Brown | J125-1 | Q104 |
| 2 | Red-Black | J125-2 | Q108 |
| 3 | Red-Orange | J125-4 | Q103 |
| 4 | Red-Yellow | J125-5 | Q107 |
| 5 | Red-Green | J125-6 | Q102 |
| 6 | Red-Blue | J125-7 | Q106 |
| 7 | Red-Violet | J125-8 | Q101 |
| 8 | Red-Gray | J125-9 | Q105 |

The row header prints the connector-pin and the transistor on one line (`J125-1 Q104`). The row pins skip `J125-3`
(row 2 is `J125-2`, row 3 is `J125-4`).

## Matrix cells

Each cell prints its description (multi-line text joined here by single spaces) and the two-digit lamp number in
its bottom-right corner, column digit first, row digit second. Double quotation marks are printed as straight
quotes.

| Row | Col 1 | Col 2 | Col 3 | Col 4 |
| --- | --- | --- | --- | --- |
| 1 | 11 20 POINTS | 21 POWER HOOPS | 31 MULTIBALL HOOPS | 41 CHAMPION RING 1 |
| 2 | 12 FREE THROW | 22 FASTBREAK COMBO | 32 RUN & SHOOT HOOPS | 42 CHAMPION RING 2 |
| 3 | 13 3 POINTS | 23 ALLEY OOP COMBO | 33 HOOK SHOT HOOPS | 43 RIGHT RETURN LANE |
| 4 | 14 2 POINTS | 24 SLAM DUNK COMBO | 34 HALF COURT HOOPS | 44 CHAMPION RING 4 |
| 5 | 15 FIELD GOALS | 25 COMBOS | 35 LIGHT TIP-OFF | 45 CHAMPION RING 3 |
| 6 | 16 MULTIBALLS | 26 TROPHY | 36 RIGHT "IN THE PAINT" | 46 LOWER RIGHT STANDUP |
| 7 | 17 SHOOT AROUND | 27 TIP-OFF COMBO | 37 SHOO(T) | 47 UPPER RIGHT STANDUP |
| 8 | 18 AROUND THE WORLD | 28 STADIUM GOODIES | 38 LEFT RETURN LANE | 48 LEFT OUTLANE |

| Row | Col 5 | Col 6 | Col 7 | Col 8 |
| --- | --- | --- | --- | --- |
| 1 | 51 SODA | 61 RAMPS: 3 POINTS (2) | 71 LEFT LIGHT FASTBREAK | 81 LIGHT ALLEY OOP |
| 2 | 52 QUESTION | 62 TIP-OFF | 72 SLAM DUNK | 82 LEFT "IN THE PAINT" |
| 3 | 53 HOT DOG | 63 FASTBREAK | 73 S(H)OOT | 83 (S)HOOT |
| 4 | 54 PIZZA | 64 ALLEY OOP | 74 RIGHT LIGHT FASTBREAK | 84 (3)PT |
| 5 | 55 CRAZY BOB'S | 65 FREE THROW | 75 LIGHT SLAM DUNK | 85 3(P)T |
| 6 | 56 EXTRA BALL | 66 SH(O)OT | 76 SHO(O)T | 86 3P(T) |
| 7 | 57 RIGHT OUTLANE | 67 IN THE PAINT 4 | 77 IN THE PAINT 1 | 87 BALL LAUNCH |
| 8 | 58 SHOOT AGAIN | 68 IN THE PAINT 3 | 78 IN THE PAINT 2 | 88 START BUTTON |

Notes on the cell text:

- Cell 61 prints three lines: `RAMPS:` / `3` / `POINTS (2)`.
- The Champion Ring lamps are numbered 1, 2, 4, 3 down column 4 (cells 41, 42, 44, 45); cell 43 is `RIGHT RETURN
  LANE`. The `IN THE PAINT` lamps are 4, 3 in column 6 (67, 68) and 1, 2 in column 7 (77, 78); `LEFT "IN THE PAINT"`
  is 82 and `RIGHT "IN THE PAINT"` is 36.
- The parenthesised letters in `SHOO(T)`, `S(H)OOT`, `(S)HOOT`, `SH(O)OT`, `SHO(O)T` (cells 37, 73, 83, 66, 76)
  and in `(3)PT`, `3(P)T`, `3P(T)` (cells 84, 85, 86) are printed exactly so; they spell SHOOT and 3PT.
- Cell 16 `MULTIBALLS` fills the whole width of its cell and touches the cell border on both sides.

## Footnote

`J1XX = Power Driver Board` (printed below the table, left).

## The Section 3 reprint (May edition, PDF page 71, printed page `3-4`)

The May edition prints this matrix a second time as `LAMP MATRIX` on PDF page 71, left half, printed `3-4`, with the
`LAMP MATRIX CIRCUIT` drawing and explanatory text below it. Every header and cell on the reprint was compared with the
`2-49` reading above and agrees, including cell 66 `SH(O)OT`, cell 61 `RAMPS: 3 POINTS (2)`, the row headers
`J125-1 Q104`, `J125-2 Q108`, `J125-4 Q103`, `J125-5 Q107`, `J125-6 Q102`, `J125-7 Q106`, `J125-8 Q101`, `J125-9 Q105`, and the
column headers `J121-1 Q96` ... `J121-9 Q97`. The circuit drawing prints a `Column (example)` circuit (`J102`, `LS240`, `LS374`, `ULN-2803` (point `A`), `560`, `1.2K` to `+18V`, `TIP107` (point `B`), `J1XX` `Yellow-XXX` to a lamp and a diode on the `PLAYFIELD`) and a `Row (example)` circuit (`J1XX` `Red-XXX`, `LS74` with `D`, `CLK`, `Q` (point `F`), `G`, `1K`, `TIP102` (point `E`), `.22`, `2.2K`, `.1mf`, `1.4V ref`, `LM339` (point `C`, `D`), `10K` to `VCC`), with truth tables `COLUMN | A | B`: `H L OFF`, `L H ON` and `ROW | C D E F G`: `NORMAL H L H L H OFF`, `OPERATION H L L H L ON`. The text beneath reads: `The microprocessor sends a signal to the column circuit causing  the output of the UNL-2803 to toggle. When point "A" drops low, the TIP107 transistor conducts and point "B" changes to a high state. At the same time, the microprocessor drives the input of the 74LS74 low, causing a high at output "F". A high state at the base of the TIP102 causes the transistor to conducts, bringing the row circuit to ground and turning the lamp on. The microprocessor changes the input of the 74LS74 to a high state to turn the lamp off. In overcurrent conditions, the lamp is shut off through the comparator. If the voltage at the negative input of the LM339 rises above 1.4V, the output changes to a low, which is fed back to the 74LS74 and shuts the circuit off.` (printed typos `UNL-2803` and `to conducts` are as shown).

## Differences between the March and May printings of this table

One difference in the text of the 64 cells: cell 66 prints `SH(O)OT` in the May edition and `SH(Q)OT` in the March
edition (the March glyph inside the brackets is a clear `Q`, including its tail, on the 300 dpi scan). Every other
cell, every wire, connector-pin and transistor in the column and row headers, and the footnote, agree. The other difference is the title-line drawing: the March page prints a diode between the lamp and `Red`, the May `2-49` page prints a dash there (the May `3-4` reprint prints the diode). The printed folio is `2-49` in May (right half of the spread) and `2-47` in March (March PDF page 125, where the Lamp Matrix precedes the Switch Matrix `2-48`).

## Uncertain readings

None in this table. (Cell 66's March reading `SH(Q)OT` is certain as printed but is probably a typographical error
for `SH(O)OT`.)
