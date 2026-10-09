# Williams Black Knight (game 500) - Lamp Matrix (two printings)

Source: `Williams_1980_Black_Knight_English_Manual_with_paginated_schematics.pdf` (IPDB 310).

- **Part A**: PDF page 69, the upper table of the separate printed sheet (the `Switch Matrix` is the lower table). No printed page number is visible. Italic caption under the table: `Lamp Matrix`. Read from the 600 dpi render `render\man600-69.png` (upright, no rotation), nine tiles (`crops2\lm-*.png`).
- **Part B**: PDF page 14 = booklet printed page `9`, caption `Figure 1. Lamp Matrix`. Printed sideways; rotated 270 degrees with PIL (`Image.rotate(270, expand=True)`), verified upright. Read from the 300 dpi render `render\man300-14.png` at native resolution (`crops2\blm-*.png`).
- Normalization: none. Capitals as printed; line breaks inside a cell shown as ` / `. The lamp matrix cells carry **no lamp numbers** (unlike the switch matrix). Italic bold `MAGNA-SAVE` is followed by a small raised quote-like mark (looks like a trademark sign); it is written `MAGNA- / SAVE"` below: printed italic bold, with a trailing superscript mark that resolves only as a small `"`-like glyph in both printings [uncertain: `TM` mark vs. quotation mark]. `"2"` ... `"10"` bonus values are printed in quotation marks, as shown.
- Part A and Part B cell text agree everywhere (see the differences section); the two printings are transcribed together below only where identical, and separately only for the header block.

## Column headers (both printings, as printed: column number, wire colour, 2J5 pin)

| Column | Wire colour | Connector pin |
|---|---|---|
| 1 | YEL-BRN | 2J5-8 |
| 2 | YEL-RED | 2J5-9 |
| 3 | YEL-ORN | 2J5-6 |
| 4 | YEL-BLK | 2J5-7 |
| 5 | YEL-GRN | 2J5-3 |
| 6 | YEL-BLU | 2J5-5 |
| 7 | YEL-VIO | 2J5-1 |
| 8 | YEL-GRY | 2J5-2 |

(2J5 pin 4 is not printed on the matrix.)

## Row headers (both printings; wire colour printed as `RED-` / colour on two lines)

| Row | Wire colour | Connector pin |
|---|---|---|
| 1 | RED-BRN | 2J7-1 |
| 2 | RED-BLK | 2J7-2 |
| 3 | RED-ORN | 2J7-3 |
| 4 | RED-YEL | 2J7-4 |
| 5 | RED-GRN | 2J7-5 |
| 6 | RED-BLU | 2J7-6 |
| 7 | RED-VIO | 2J7-9 |
| 8 | RED-GRY | 2J7-8 |

(Row 7 is pin 2J7-9 and row 8 is pin 2J7-8; pin 2J7-7 is not printed. This order 9, 8 is as printed in both printings.)

## Part A - PDF page 69 Lamp Matrix: cells (64 of 64)

| Row \ Column | 1 YEL-BRN 2J5-8 | 2 YEL-RED 2J5-9 | 3 YEL-ORN 2J5-6 | 4 YEL-BLK 2J5-7 |
|---|---|---|---|---|
| 1 RED-BRN 2J7-1 | SAME / PLAYER / SHOOTS / AGAIN | RIGHT / *MAGNA- / SAVE"* / LAMP | BOTTOM / LEFT / 3-BANK / LAMP | BOTTOM / LEFT / 3-BANK, / LOWER ARROW |
| 2 RED-BLK 2J7-2 | BALL / IN / PLAY | LEFT / *MAGNA- / SAVE"* / LAMP | BOTTOM / RIGHT / 3-BANK / LAMP | BOTTOM / LEFT / 3-BANK / CENTER ARROW |
| 3 RED-ORN 2J7-3 | TILT | LEFT / OUTLANE | TOP / LEFT / 3-BANK / LAMP | BOTTOM / LEFT / 3-BANK / UPPER ARROW |
| 4 RED-YEL 2J7-4 | GAME / OVER | RIGHT / OUTLANE | TOP / RIGHT / 3-BANK / LAMP | 2X / SCORING |
| 5 RED-GRN 2J7-5 | MATCH | RIGHT / SPINNER | CENTER / LOCK / LAMP | BOTTOM / RIGHT / 3-BANK, / RIGHT ARROW |
| 6 RED-BLU 2J7-6 | HIGH / SCORE / TO / DATE | RAMP / ROLLUNDER | TURNAROUND / EXTRA / BALL / WHEN LIT | BOTTOM / RIGHT / 3-BANK, / CENTER ARROW |
| 7 RED-VIO 2J7-9 | CREDITS / (PLAY- / FIELD) | RIGHT / INSIDE / ROLLOVER | TURNAROUND / SPECIAL | BOTTOM / RIGHT / 3-BANK, / LEFT ARROW |
| 8 RED-GRY 2J7-8 | BONUS / BALL / TIME | LEFT / INSIDE / ROLLOVER | LOWER / PLAYFIELD / EJECT / HOLE | 3X / SCORING |

| Row \ Column | 5 YEL-GRN 2J5-3 | 6 YEL-BLU 2J5-5 | 7 YEL-VIO 2J5-1 | 8 YEL-GRY 2J5-2 |
|---|---|---|---|---|
| 1 RED-BRN 2J7-1 | TOP / LEFT / 3-BANK / LOWER ARROW | LEFT RAMP / ROLLUNDER / EXTRA BALL / WHEN LIT | "2" / BONUS | "10" / BONUS |
| 2 RED-BLK 2J7-2 | TOP / LEFT / 3-BANK / CENTER ARROW | LEFT / LOCK / LAMP | "3" / BONUS | "20" / BONUS |
| 3 RED-ORN 2J7-3 | TOP / LEFT / 3-BANK / UPPER ARROW | NOT / USED | "4" / BONUS | "30" / BONUS |
| 4 RED-YEL 2J7-4 | JET / BUMPER | NOT / USED | "5" / BONUS | "40" / BONUS |
| 5 RED-GRN 2J7-5 | TOP / RIGHT / 3-BANK / LOWER ARROW | NOT / USED | "6" / BONUS | 2x |
| 6 RED-BLU 2J7-6 | TOP / RIGHT / 3-BANK / CENTER ARROW | NOT / USED | "7" / BONUS | 3x |
| 7 RED-VIO 2J7-9 | TOP / RIGHT / 3-BANK / UPPER ARROW | SAME PLAYER / SHOOTS / AGAIN / (PLAYFIELD) | "8" / BONUS | 4x |
| 8 RED-GRY 2J7-8 | RIGHT / LOCK / LAMP | "1" / BONUS | "9" / BONUS | 5x |

Notes on the Part A cells: the bonus lamps in column 7 read `"2"` ... `"9"` top to bottom, `"1"` is in column 6 row 8, `"10"`, `"20"`, `"30"`, `"40"` fill column 8 rows 1-4, and the multiplier lamps `2x`, `3x`, `4x`, `5x` (lowercase `x`) fill column 8 rows 5-8. The `2X SCORING` and `3X SCORING` cells (column 4 rows 4 and 8) use capital `X`. No cell in the lamp matrix is blank; the "not used" cells are all printed `NOT USED` (column 6 rows 3-6).

## Part B - PDF page 14 (booklet printed page 9), `Figure 1. Lamp Matrix`: cells (64 of 64)

The 64 cells and 16 headers of Part B, read from the rotated 300 dpi render, are letter-for-letter identical to Part A including line breaks, the comma placements (`3-BANK,` with a comma in column 4 rows 1, 5, 6, 7; no comma after `3-BANK` in column 4 rows 2 and 3 nor in any column 3 or column 5 cell), the quotation marks around the bonus numbers, and the italic bold `MAGNA-SAVE` in cells (row 1, column 2) and (row 2, column 2). Part B headers: `COLUMN` / `ROW` corner, columns `1 YEL-BRN 2J5-8`, `2 YEL-RED 2J5-9`, `3 YEL-ORN 2J5-6`, `4 YEL-BLK 2J5-7`, `5 YEL-GRN 2J5-3`, `6 YEL-BLU 2J5-5`, `7 YEL-VIO 2J5-1`, `8 YEL-GRY 2J5-2`; rows `1 RED-BRN 2J7-1`, `2 RED-BLK 2J7-2`, `3 RED-ORN 2J7-3`, `4 RED-YEL 2J7-4`, `5 RED-GRN 2J7-5`, `6 RED-BLU 2J7-6`, `7 RED-VIO 2J7-9`, `8 RED-GRY 2J7-8`.

## Differences between Part A and Part B

None found in the cell text, wire colours or connector pins (checked on all 64 cells and all 16 headers). The only differences are physical: Part B is rotated on its page and carries a printed page number `9` and caption `Figure 1. Lamp Matrix`; Part A has no printed page number and the caption `Lamp Matrix`. The `"2"` bonus cell's quote marks are slightly clearer in Part A.

## Observations

- Row 7 and row 8 connector pins read `2J7-9` and `2J7-8` in both printings (descending, with 2J7-7 skipped). This is the printed order, not a transcription slip.
- The lamp matrix prints no lamp numbers; the lamp number for a cell is not stated on this sheet.
- Cells that read `NOT USED`: column 6 rows 3, 4, 5, 6 (four cells), in both printings.
- Titles: the matrix cell `CREDITS (PLAY-FIELD)` is a hyphenated line break (`(PLAY-` / `FIELD)`), written `(PLAYFIELD)` elsewhere (cell column 6 row 7 `(PLAYFIELD)` is not hyphenated).
