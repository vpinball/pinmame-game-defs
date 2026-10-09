# Williams Black Knight (game 500) - Switch Matrix (two printings)

Source: `Williams_1980_Black_Knight_English_Manual_with_paginated_schematics.pdf` (IPDB 310).

- **Part A**: PDF page 69, a separate printed sheet carrying the `Lamp Matrix` (upper) and `Switch Matrix` (lower). No printed page number is visible on the sheet (only a bottom rule). Italic caption under the table: `Switch Matrix`. Read from the 600 dpi render `render\man600-69.png` (upright, no rotation), cropped into six tiles at 1.0-0.76 scale (`crops2\sw-*.png`).
- **Part B**: PDF page 18 = booklet printed page `13`, caption `Figure 5. Switch Matrix`. The figure is printed sideways; rotated 270 degrees with PIL (`Image.rotate(270, expand=True)`) so it reads upright (verified: headers and cell text upright afterwards). Read from the 300 dpi render `render\man300-18.png` at native resolution (`crops2\bsw-*.png`).
- Normalization: none. Text is transcribed as printed in capitals; line breaks inside a cell are shown with ` / `. Each cell carries a bold switch number at its lower-right corner. Every cell below is `function text` + `[number]`. "NOT USED" cells are transcribed as printed (some add `STANDUP` on a third line).
- A stray pen arc (curved hairline) is drawn through the cells 45, 46, 47 region on the booklet printing only (Part B); it is not part of the table and does not alter a cell.

## Part A - PDF page 69 Switch Matrix

Corner cell: `COLUMN` (upper right) / `ROW` (lower left), separated by a diagonal.

### Column headers (as printed: column number, wire colour, 2J2 pin)

| Column | Wire colour | Connector pin |
|---|---|---|
| 1 | GRN-BRN | 2J2-9 |
| 2 | GRN-RED | 2J2-8 |
| 3 | GRN-ORN | 2J2-7 |
| 4 | GRN-YEL | 2J2-6 |
| 5 | GRN-BLK | 2J2-5 |
| 6 | GRN-BLU | 2J2-3 |
| 7 | GRN-VIO | 2J2-2 |
| 8 | GRN-GRY | 2J2-1 |

(There is no 2J2-4 column: pin 4 is not printed on this matrix.)

### Row headers (as printed: row number, wire colour printed as `WHT-` / colour on two lines, 2J3 pin)

| Row | Wire colour | Connector pin |
|---|---|---|
| 1 | WHT-BRN | 2J3-9 |
| 2 | WHT-RED | 2J3-8 |
| 3 | WHT-ORN | 2J3-7 |
| 4 | WHT-YEL | 2J3-6 |
| 5 | WHT-GRN | 2J3-5 |
| 6 | WHT-BLU | 2J3-4 |
| 7 | WHT-VIO | 2J3-3 |
| 8 | WHT-GRY | 2J3-1 |

(There is no 2J3-2 row: pin 2 is not printed on this matrix.)

### Cells (64 of 64)

| Row \ Column | 1 GRN-BRN 2J2-9 | 2 GRN-RED 2J2-8 | 3 GRN-ORN 2J2-7 | 4 GRN-YEL 2J2-6 |
|---|---|---|---|---|
| 1 WHT-BRN 2J3-9 | PLUMB / BOB / TILT [1] | RIGHT / MAGNET / BUTTON [9] | RIGHT / BALL / RAMP [17] | LOWER LEFT / 3-BANK, / LOWER / TARGET [25] |
| 2 WHT-RED 2J3-8 | BALL / ROLL / TILT [2] | LEFT / MAGNET / BUTTON [10] | CENTER / BALL / RAMP / TARGET [18] | LOWER LEFT / 3-BANK, / CENTER / TARGET [26] |
| 3 WHT-ORN 2J3-7 | CREDIT / BUTTON [3] | LEFT / OUTLANE [11] | LEFT / BALL / RAMP [19] | LOWER LEFT / 3-BANK, / UPPER / TARGET [27] |
| 4 WHT-YEL 2J3-6 | RIGHT / COIN / SWITCH [4] | RIGHT / OUTLANE [12] | OUTHOLE [20] | NOT / USED / STANDUP [28] |
| 5 WHT-GRN 2J3-5 | CENTER / COIN / SWITCH [5] | LEFT / SPINNER [13] | LOWER / KICKER / 3-BANK, / LEFT TARGET [21] | LOWER / RIGHT / 3-BANK / RIGHT TARGET [29] |
| 6 WHT-BLU 2J3-4 | LEFT / COIN / SWITCH [6] | RIGHT / RAMP / ROLLUNDER [14] | RIGHT / KICKER [22] | LOWER / RIGHT / 3-BANK, / CENTER TARGET [30] |
| 7 WHT-VIO 2J3-3 | SLAM / TILT [7] | RIGHT / INSIDE / ROLLOVER [15] | TURNAROUND [23] | LOWER / RIGHT / 3-BANK, / LEFT TARGET [31] |
| 8 WHT-GRY 2J3-1 | HIGH / SCORE / RESET [8] | LEFT / INSIDE / ROLLOVER [16] | LOWER / PLAYFIELD / EJECT / HOLE [24] | NOT / USED / STANDUP [32] |

| Row \ Column | 5 GRN-BLK 2J2-5 | 6 GRN-BLU 2J2-3 | 7 GRN-VIO 2J2-2 | 8 GRN-GRY 2J2-1 |
|---|---|---|---|---|
| 1 WHT-BRN 2J3-9 | TOP LEFT / 3-BANK / LOWER / TARGET [33] | LOCKUP / TROUGH, / BOTTOM [41] | NOT / USED [49] | NOT / USED [57] |
| 2 WHT-RED 2J3-8 | TOP LEFT / 3-BANK / CENTER / TARGET [34] | LOCKUP / TROUGH, / CENTER [42] | NOT / USED [50] | NOT / USED [58] |
| 3 WHT-ORN 2J3-7 | TOP LEFT / 3-BANK / UPPER / TARGET [35] | LOCKUP / TROUGH, / TOP [43] | NOT / USED [51] | NOT / USED [59] |
| 4 WHT-YEL 2J3-6 | JET / BUMPER [36] | LEFT / RAMP / ROLLOVER [44] | NOT / USED [52] | NOT / USED [60] |
| 5 WHT-GRN 2J3-5 | TOP / RIGHT / 3-BANK / LOWER TARGET [37] | BALLSHOOTER / TROUGH [45] | NOT / USED [53] | NOT / USED [61] |
| 6 WHT-BLU 2J3-4 | TOP / RIGHT / 3-BANK / CENTER TARGET [38] | PLAYFIELD / TILT [46] | NOT / USED [54] | NOT / USED [62] |
| 7 WHT-VIO 2J3-3 | TOP / RIGHT / 3-BANK / UPPER TARGET [39] | NOT / USED [47] | NOT / USED [55] | NOT / USED [63] |
| 8 WHT-GRY 2J3-1 | NOT / USED / STANDUP [40] | NOT / USED [48] | NOT / USED [56] | NOT / USED [64] |

Cell number = (column - 1) * 8 + row holds for every cell.

## Part B - PDF page 18 (booklet printed page 13), `Figure 5. Switch Matrix`

Headers: corner `COLUMN` / `ROW`; column headers `1 GRN-BRN 2J2-9`, `2 GRN-RED 2J2-8`, `3 GRN-ORN 2J2-7`, `4 GRN-YEL 2J2-6`, `5 GRN-BLK 2J2-5`, `6 GRN-BLU 2J2-3`, `7 GRN-VIO 2J2-2`, `8 GRN-GRY 2J2-1`; row headers `1 WHT-BRN 2J3-9`, `2 WHT-RED 2J3-8`, `3 WHT-ORN 2J3-7`, `4 WHT-YEL 2J3-6`, `5 WHT-GRN 2J3-5`, `6 WHT-BLU 2J3-4`, `7 WHT-VIO 2J3-3`, `8 WHT-GRY 2J3-1`. All 16 headers are identical to Part A.

### Cells (64 of 64)

| Row \ Column | 1 | 2 | 3 | 4 |
|---|---|---|---|---|
| 1 | PLUMB / BOB / TILT [1] | RIGHT / MAGNET / BUTTON [9] | RIGHT / BALL / RAMP [17] | LOWER LEFT / 3-BANK, / LOWER / TARGET [25] |
| 2 | BALL / ROLL / TILT [2] | LEFT / MAGNET / BUTTON [10] | CENTER / BALL / RAMP / TARGET [18] | LOWER LEFT / 3-BANK, / CENTER / TARGET [26] |
| 3 | CREDIT / BUTTON [3] | LEFT / OUTLANE [11] | LEFT / BALL / RAMP [19] | LOWER LEFT / 3-BANK, / UPPER / TARGET [27] |
| 4 | RIGHT / COIN / SWITCH [4] | RIGHT / OUTLANE [12] | OUTHOLE [20] | NOT / USED / STANDUP [28] |
| 5 | CENTER / COIN / SWITCH [5] | LEFT / SPINNER [13] | LOWER / KICKER / 3-BANK, / LEFT TARGET [21] | LOWER / RIGHT / 3-BANK / RIGHT TARGET [29] |
| 6 | LEFT / COIN / SWITCH [6] | RIGHT / RAMP / ROLLUNDER [14] | RIGHT / KICKER [22] | LOWER / RIGHT / 3-BANK, / CENTER TARGET [30] |
| 7 | SLAM / TILT [7] | RIGHT / INSIDE / ROLLOVER [15] | TURNAROUND [23] | LOWER / RIGHT / 3-BANK, / LEFT TARGET [31] |
| 8 | HIGH / SCORE / RESET [8] | LEFT / INSIDE / ROLLOVER [16] | LOWER / PLAYFIELD / EJECT / HOLE [24] | NOT / USED / STANDUP [32] |

| Row \ Column | 5 | 6 | 7 | 8 |
|---|---|---|---|---|
| 1 | TOP LEFT / 3-BANK / LOWER / TARGET [33] | LOCKUP / TROUGH, / BOTTOM [41] | NOT / USED [49] | NOT / USED [57] |
| 2 | TOP LEFT / 3-BANK / CENTER / TARGET [34] | LOCKUP / TROUGH, / CENTER [42] | NOT / USED [50] | NOT / USED [58] |
| 3 | TOP LEFT / 3-BANK / UPPER / TARGET [35] | LOCKUP / TROUGH, / TOP [43] | NOT / USED [51] | NOT / USED [59] |
| 4 | JET / BUMPER [36] | LEFT / RAMP / ROLLOVER [44] | NOT / USED [52] | NOT / USED [60] |
| 5 | TOP / RIGHT / 3-BANK / LOWER TARGET [37] | BALLSHOOTER / TROUGH [45] | NOT / USED [53] | NOT / USED [61] |
| 6 | TOP / RIGHT / 3-BANK / CENTER TARGET [38] | PLAYFIELD / TILT [46] | NOT / USED [54] | NOT / USED [62] |
| 7 | TOP / RIGHT / 3-BANK / UPPER TARGET [39] | NOT / USED [47] | NOT / USED [55] | NOT / USED [63] |
| 8 | NOT / USED / STANDUP [40] | NOT / USED [48] | NOT / USED [56] | NOT / USED [64] |

## Differences between Part A and Part B

Cell-by-cell comparison of all 64 cells, 8 column headers and 8 row headers: **no difference in wording, switch number, wire colour or connector pin was found.**

Only variations noted, none of them differences in content:

1. Cell 29 (column 4, row 5) is printed `LOWER / RIGHT / 3-BANK / RIGHT TARGET` with no comma after `3-BANK` in both printings, whereas cells 30 and 31 (same column, rows 6 and 7) print `3-BANK,` with a comma in both printings. This is an inconsistency inside the table (identical in both printings), not a difference between them. The same comma-less form is printed for cells 37, 38, 39 (`TOP / RIGHT / 3-BANK / ...`).
2. A pen arc mark (Part B only) crosses the 45/46/47 area; not content.

## Observations

- Cells 28, 32 and 40 are printed `NOT USED STANDUP` (a third line `STANDUP`), whereas the other not-used cells (47-64) are printed `NOT USED` only. Identical in both printings.
- Switch numbers run column-major: cell number = 8 * (column - 1) + row, for all 64 cells in both printings (checked).
- The wire colours of the columns are all `GRN-xxx`, of the rows all `WHT-xxx`; the column wire colour sequence BRN, RED, ORN, YEL, BLK, BLU, VIO, GRY follows 2J2 pins 9, 8, 7, 6, 5, 3, 2, 1 (pin 4 skipped); the rows follow BRN, RED, ORN, YEL, GRN, BLU, VIO, GRY on 2J3 pins 9, 8, 7, 6, 5, 4, 3, 1 (pin 2 skipped). Note that the row colour for row 5 is `GRN` (`WHT-GRN`), printed as `WHT-` over `GRN`.
- A small stray dot appears beside the row-4 header on the Part A scan (scan noise).
- Counts: Part A 64 cells + 8 column headers + 8 row headers; Part B 64 cells + 8 + 8.
