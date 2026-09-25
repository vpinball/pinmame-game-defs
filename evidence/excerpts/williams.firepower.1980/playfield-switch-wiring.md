# Williams Firepower (game 497) — Playfield Switch Wiring Diagram

Source: `Williams_1980_Firepower_Schematics_paginated_from_manual_dated_March_1980.pdf` (IPDB 856),
PDF page 26, printed page 26, sheet marked `497`. The sheet is printed sideways. Transcribed by hand
from a 300 dpi render.

Headings, verbatim: `FIRE POWER` / `PLAYFIELD SWITCH WIRING DIAGRAM`; caption
`Playfield Switch Wiring Diagram`.

## Function list printed on the sheet

`SWITCH NO. FUNCTION`, 09 to 58, identical in wording to the booklet's Figure 4 chart except that
switches 17, 18, 19, 21, 22 and 23 are printed `"1" Drop Target`, `"2" Drop Target`,
`"3" Drop Target`, `"4" Drop Target`, `"5" Drop Target` and `"6" Drop Target` (the booklet prints
`Target`), 27 is printed correctly as `Top Right Jet Bumper`, no scores are given, and 20, 24, 52,
55 and 56 are printed `Not Used`.

## Matrix drawing

Every switch is drawn as a normally open contact labelled `8SWn` with a series diode `8Dn`
(`n` = switch number). Positions drawn, by column:

| Column | Switches drawn | Positions not drawn |
| --- | --- | --- |
| 2 | 8SW9 to 8SW16 | none |
| 3 | 8SW17, 18, 19, 21, 22, 23 | 20, 24 |
| 4 | 8SW25 to 8SW32 | none |
| 5 | 8SW33 to 8SW40 | none |
| 6 | 8SW41 to 8SW48 | none |
| 7 | 8SW49, 50, 51, 53, 54 | 52, 55, 56 |
| 8 | 8SW57, 8SW58 | 59 to 64 |

Column 1 (switches 1-8) is not on this sheet; it is cabinet wiring (see `cabinet-wiring.md`).
The diode beside 8SW54 carries no label. The labels `8SW15`/`8D15`, `8SW39`/`8D39`,
`8SW57`/`8D57`, `8SW58`/`8D58` and the heading `COLUMN 8` are lettered in a lighter, smaller
typeface than the rest of the sheet, as later additions.

## Harness connectors

| Line | Driver board | Wire | Playfield 8P1/8J1 pin |
| --- | --- | --- | --- |
| COLUMN 2 | 2J2-8 | GRN-RED | 1 |
| COLUMN 3 | 2J2-7 | GRN-ORG | 2 |
| COLUMN 4 | 2J2-6 | GRN-YEL | 3 |
| COLUMN 5 | 2J2-5 | GRN-BLK | 4 |
| COLUMN 6 | 2J2-3 | GRN-BLU | 5 |
| COLUMN 7 | 2J2-2 | GRN-VIO | 6 |
| COLUMN 8 | 2J2-1 | GRN-GRY | 7 |
| ROW 1 | 2J3-9 | WHT-BRN | 8 |
| ROW 2 | 2J3-8 | WHT-RED | 9 |
| ROW 3 | 2J3-7 | WHT-ORG | 10 |
| ROW 4 | 2J3-6 | WHT-YEL | 11 |
| ROW 5 | 2J3-5 | WHT-GRN | 12 |
| ROW 6 | 2J3-4 | WHT-BLU | 13 |
| ROW 7 | 2J3-3 | WHT-VIO | 14 |
| ROW 8 | 2J3-1 | WHT-GRY | 15 |

The driver-board side is labelled `PART OF DRIVER BOARD` twice, once for 2J2/2P2 and once for
2J3/2P3.
