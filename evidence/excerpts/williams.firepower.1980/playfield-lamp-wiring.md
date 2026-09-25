# Williams Firepower (game 497) — Playfield Lamp Wiring Diagram

Source: `Williams_1980_Firepower_Schematics_paginated_from_manual_dated_March_1980.pdf` (IPDB 856),
PDF page 27, printed page 27, sheet marked `497`. The sheet is printed sideways. Transcribed by hand
from a 300 dpi render.

Headings, verbatim: `FIRE POWER` / `PLAYFIELD LAMP WIRING DIAGRAM`; caption
`Playfield Lamp Wiring Diagram`.

## Bulb list printed on the sheet

`BULB NO. FUNCTION`

| Bulb | Function |
| --- | --- |
| 1 | Same Player Shoots |
| 2 | Ball Saver Kicker On |
| 3 | FIRE (x2) |
| 4 | POWER (x2) |
| 5 | "F" |
| 6 | "I" |
| 7 | "R" |
| 8 | "E" |
| 9 | Top POWER Target |
| 10 | Center POWER Target |
| 11 | Bottom POWER Target |
| 12 | Right Inside Rollover |
| 13 | Left Inside Rollover |
| 14 | 1000 Bonus |
| 15 | 2000 Bonus |
| 16 | 3000 Bonus |
| 17 | 4000 Bonus |
| 18 | 5000 Bonus |
| 19 | 6000 Bonus |
| 20 | 7000 Bonus |
| 21 | 8000 Bonus |
| 22 | 9000 Bonus |
| 23 | Not Used |
| 24 | 10,000 Bonus |
| 25 | 20,000 Bonus |
| 26 | "1" Drop Target Arrow |
| 27 | "2" Drop Target Arrow |
| 28 | "3" Drop Target Arrow |
| 29 | "4" Drop Target Arrow |
| 30 | "5" Drop Target Arrow |
| 31 | "6" Drop Target Arrow |
| 32 | Spinner 1000 When Lit |
| 33 | Left Eject Hole Arrow |
| 34 | Right Eject Hole Arrow |
| 35 | Upper Right Eject Hole Arrow |
| 36 | 2X |
| 37 | 3X |
| 38 | 4X |
| 39 | 5X |
| 40 | Extra Ball When Lit |
| 41 | 10,000 FIREPOWER Bonus |
| 42 | 30,000 FIREPOWER Bonus |
| 43 | 50,000 FIREPOWER Bonus |
| 44 | Top Left Jet Bumper |
| 45 | Top Right Jet Bumper |
| 46 | Bottom Right Jet Bumper |
| 47 | Bottom Left Jet Bumper |
| 48 | Left Special |
| 49 | Right Special |
| 56 | Credits (Playfield) |

The list jumps from 49 to 56: bulbs 50-55 and 57-64 are backbox lamps on the insert board (see
`insert-board-wiring.md`). Entries 26-31 say `Drop Target Arrow` where the booklet's Figure 6 says
`TARGET ARROW`. The numbers 49 and 56 are partly overwritten by a hand-drawn bracket.

## Matrix drawing

Each bulb is drawn as `8Bn` with a series diode `8D(64+n)`. Drawn positions, by column:

| Column | Bulbs drawn | Diodes |
| --- | --- | --- |
| 1 | 8B1 to 8B8 | 8D65 to 8D72 |
| 2 | 8B9 to 8B15, then a second bulb labelled `8B15` | 8D73 to 8D80 |
| 3 | 8B17 to 8B22, 8B24 (no bulb in the row-7 position) | 8D81 to 8D86, 8D88 |
| 4 | 8B25 to 8B30, a bulb labelled `8B31`, 8B32 | 8D89 to 8D96 |
| 5 | 8B33 to 8B40 | 8D97 to 8D104 |
| 6 | 8B41 to 8B48 | 8D105 to 8D112 |
| 7 | a bulb labelled `8B47` in row 1 and `8B56` in row 8 | 8D113, 8D120 |

Three bulb labels are lettered in the lighter, smaller hand of later additions and one of them is
wrong. The second `8B15` in column 2 sits in the row-8 position with diode `8D80`, so it is bulb 16.
The row-1 bulb of column 7 is labelled `8B47` but carries diode `8D113` and sits where bulb 49
(Right Special) belongs; the real 8B47 is drawn in column 6 with `8D111`. `8B31` with `8D95` is
correct. The row-7 position of column 3 (bulb 23) is left empty.

Column 8 is not on this sheet.

## Harness connectors

| Line | Driver board | Wire | Playfield 8P2/8J2 pin |
| --- | --- | --- | --- |
| COLUMN 1 | 2J5-8 | YEL-BRN | 3 |
| COLUMN 2 | 2J5-9 | YEL-RED | 4 |
| COLUMN 3 | 2J5-6 | YEL-ORG | 5 |
| COLUMN 4 | 2J5-7 | YEL-BLK | 6 |
| COLUMN 5 | 2J5-3 | YEL-GRN | 7 |
| COLUMN 6 | 2J5-5 | YEL-BLU | 8 |
| COLUMN 7 | 2J5-1 | YEL-VIO | 9 |
| ROW 1 | 2J7-1 | RED-BRN | 11 |
| ROW 2 | 2J7-2 | RED-BLK | 12 |
| ROW 3 | 2J7-3 | RED-ORG | 13 |
| ROW 4 | 2J7-4 | RED-YEL | 14 |
| ROW 5 | 2J7-5 | RED-GRN | 15 |
| ROW 6 | 2J7-6 | RED-BLU | 16 |
| ROW 7 | 2J7-9 | RED-VIO | 17 |
| ROW 8 | 2J7-8 | RED-GRY | 18 |

## General illumination

A dashed block labelled `GENERAL ILLUMINATION` holds a row of bulbs across `8J2`/`8P2` pins 1 and 2,
wired `YEL` and `YEL-WHT` from a `FUSE CARD` to `6.3 V.A.C. GENERAL ILLUMINATION`. No switching
device is drawn in this circuit.
