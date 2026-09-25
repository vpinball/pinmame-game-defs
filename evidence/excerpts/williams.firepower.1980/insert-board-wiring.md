# Williams Firepower (game 497) — Insert Board Wiring Diagram (backbox)

Source: `Williams_1980_Firepower_Schematics_paginated_from_manual_dated_March_1980.pdf` (IPDB 856),
PDF page 28, printed page 28, sheet marked `497`. The sheet is printed sideways. Transcribed by hand
from a 300 dpi render.

Headings, verbatim: `INSERT BOARD WIRING`, `MASTER DISPLAY P.C. BOARD`; caption
`Insert Board Wiring Diagram`.

## Insert board connector 9J1

| 9J1 pin | Printed label |
| --- | --- |
| 1 | 6.3 VAC |
| 2 | 6.3 VAC |
| 3 | N.C. |
| 4 | 6.3 VAC |
| 5 | 6.3 VAC |
| 6 | LAMP COLUMN 7 |
| 7 | LAMP COLUMN 8 |
| 8 | LAMP ROW 1 |
| 9 | LAMP ROW 2 |
| 10 | LAMP ROW 3 |
| 11 | LAMP ROW 4 |
| 12 | LAMP ROW 5 |
| 13 | LAMP ROW 6 |
| 14 | LAMP ROW 7 |
| 15 | LAMP ROW 8 |

Pins 1, 2, 4 and 5 feed a row of backbox illumination bulbs, three drawn solid and two dashed.

## Controlled backbox lamps

Each insert is drawn as a bulb with a series diode between its lamp column and its lamp row.

| Row | Column 7 insert | Column 8 insert |
| --- | --- | --- |
| 1 | (none) | "PLAYER 1 UP" |
| 2 | "1 CAN PLAY" | "PLAYER 2 UP" |
| 3 | "2 CAN PLAY" | "PLAYER 3 UP" |
| 4 | "3 CAN PLAY" | "PLAYER 4 UP" |
| 5 | "4 CAN PLAY" | "TILT" |
| 6 | "MATCH" | "GAME OVER" (two bulbs in parallel) |
| 7 | "BALL IN PLAY" | "SAME PLAYER SHOOTS" (two bulbs in parallel) |
| 8 | (none) | "HIGH SCORE" (two bulbs in parallel) |

Column 7 rows 1 and 8 are playfield lamps (Right Special and Credits (Playfield)) and are drawn on
the playfield lamp sheet instead.

## Score displays

`PLAYER #1` to `PLAYER #4`, each a six-digit display on its own board, wired from `5J1` to `5J4`;
`5J1` lists the digit, segment, key and keep-alive lines, and 5J2-5J4 are printed
`SAME CONNECTION AS 5J1`. The player boards connect over `BROWN-WHITE`/`BRN-WHT` from `9J2`-`9J5` to
`9P2`-`9P5` and on to `4P7-2`. Player #1 digits are strobes 1-6, Player #2 strobes 9-14, Player #3
strobes 1-6 and Player #4 strobes 9-14 (each display's six digits labelled `STROBE` n).

## Master display board

The master display board carries one six-position window. Its positions, left to right, are
labelled `NOT USED`, `STROBE 15`, `STROBE 16`, `NOT USED`, `STROBE 7`, `STROBE 8`: two two-digit
displays, strobes 15-16 on the left and 7-8 on the right. Connectors: `4J1`-`4J4` for the
Player #1-#4 segment and digit lines, `4J5` `STROBE INPUTS`, `4J6` `BCD INPUTS` (`B1`, `C1`,
`BLANKING`, `D1`, `A1`, `B2`, `C2`, `D2`, `A2`), and `4J7` `POWER INPUTS` (`-100 VDC`, `+100 VDC`,
`+5 VDC`, `N.C.`, `GROUND`, `-100 VDC`).
