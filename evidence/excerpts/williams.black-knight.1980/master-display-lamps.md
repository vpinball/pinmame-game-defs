# Williams Black Knight (game 500) — Insert Board / Master Display Wiring Diagram (backbox lamps)

Source: `Williams_1980_Black_Knight_English_Manual_with_paginated_schematics.pdf` (IPDB 310),
PDF pages 54 and 55 (with PDF page 53 as the upper part of the same foldout), printed caption `Insert Board Wiring Diagram`,
printed page `17` (legible on PDF page 55; on PDF page 54 only the first letters `Inse` of the caption are visible at the
page edge), sheet marked `500`. Transcribed by hand from 600 dpi renders (`pdftoppm -r 600 -gray`).

The drawing is a foldout split across consecutive scan pages: PDF pages 54 and 55 repeat the same drawing content at different
vertical offsets (the master display outline, the 4J5/4J6/4J7 connectors, the 9P1 backbox lamp wiring and the
`CREDITS / BALL IN PLAY` display appear on both; page 55 is shifted up so the 9P1 block is cut at its top). The 9P1
general-illumination and `COLUMN 1` lines are only complete on PDF page 54 (they begin again at the bottom of PDF page 53). The
drawings read upright in the unrotated landscape renders (the caption and page number run sideways), so no rotation was applied.

Heading, verbatim: `MASTER DISPLAY` (text inside the outline); no separate title block for the lamp wiring.

## Backbox lamp wiring at connector `9P1` (right of the master display outline)

Connector bar printed `9P1`. Pins printed on the bar (top to bottom): `1`, `4`, `5`, `2`, `7`, `8`, `9`, `10`, `11`, `12`, `13`, `15`
(there is no pin 3, 6 or 14 printed).

### General illumination (6.3 V.A.C.)
- Printed label on the upper line: `6.3V.A.C.`
- Pin `1` is wired to the upper horizontal line; pin `4` is wired to the same line through a short vertical jog (pins 1 and 4 are tied together).
- Pin `2` is wired to the lower horizontal line; pin `5` is wired to the same line through a short vertical jog (pins 2 and 5 are tied together).
- Fuse in the lower line between the pin-2/pin-5 node and the first lamp: `9F1` / `10A` (printed beside the fuse symbol).
- Five lamp symbols are drawn in parallel between the upper and lower lines (no designators printed): the first three are connected with solid lines, the fourth and fifth are
  connected with dashed lines and the two lines continue as dashed / dotted lines to the right edge of the drawing (running off the end
  of the printed area).
- No other label (such as a bulb number) is printed beside the five lamps.

### Lamp matrix wiring (one column, rows 1-6 and 8)
| 9P1 pin | Row/column label | Diode | Bulb | Printed legend (function) |
|---|---|---|---|---|
| 7 | COLUMN 1 | — | — | line runs right and down the right-hand edge as the common return of every bulb row below |
| 8 | ROW 1 | 9D1 | 9B1 (drawn as **two lamp symbols in parallel**, one above the other, enclosed in a rectangle with a single `9B1` designator) | SHOOT AGAIN |
| 9 | ROW 2 | 9D2 | 9B2 | BALL "IN PLAY" |
| 10 | ROW 3 | 9D3 | 9B3 | TILT |
| 11 | ROW 4 | 9D4 | 9B4 | GAME OVER |
| 12 | ROW 5 | 9D5 | 9B5 | MATCH |
| 13 | ROW 6 | 9D6 | 9B6 | HIGH SCORE |
| 15 | ROW 8 | 9D8 | 9B8 | BONUS BALL TIMER |

Each row is drawn as: 9P1 pin arrow -> row label -> diode (triangle pointing left toward the 9P1 connector, bar at its left/connector side) ->
lamp symbol -> legend text -> dot on the common vertical wire at the right edge, which is the `COLUMN 1` line from pin 7. `9B1`'s
two lamps sit between two dots joined by a rectangle; its right dot is joined to the common vertical wire.

There is no `ROW 7` label, no 9P1 pin `14`, no `9D7` and no `9B7` printed or drawn: the sequence goes `ROW 6` (pin 13) to `ROW 8` (pin 15).

The playfield lamp sheet's printed bulb list names bulb `07` `Credits (Playfield)`; no bulb carrying a 9B7/credits legend is drawn on this sheet.

## Master display outline and display connectors (same pages)

Outline labelled `MASTER DISPLAY` with edge connectors:
| Connector | Label printed beside it |
|---|---|
| 4J2 | PLAYER 2 |
| 4J1 | PLAYER 1 |
| 4J3 | PLAYER 3 |
| 4J4 | PLAYER 4 |
| 4J8 | CREDIT/MATCH |
| 4J5 | (strobe inputs, below) |
| 4J7 | (BCD inputs, below) |
| 4J6 | (power inputs, below) |

### 4J5 pins (brace label `STROBE INPUTS`), pin number then printed label
18 `COMMA 1 & 2`; 17 `STROBE 14`; 16 `STROBE 15`; 15 `STROBE 11`; 14 `STROBE 16`; 13 `STROBE 13`; 12 `STROBE 12`; 11 `STROBE 7`;
10 `STROBE 6`; 9 `STROBE 5`; 8 `STROBE 4`; 7 `STROBE 3`; 6 `STROBE 2`; 5 `STROBE 1`; 4 `STROBE 9`; 3 `STROBE 8`; 2 `STROBE 10`;
1 `COMMA 3 & 4`.

### 4J7 pins (brace label `BCD INPUTS`)
1 `B1`; 2 `C1`; 3 `BLANKING`; 4 `D1`; 5 `A1`; 6 `B2`; 7 `C2`; 8 `D2`; 9 `A2`.

### 4J6 pins (brace label `POWER INPUTS`)
1 `-100 VDC`; 2 `+100 VDC`; 3 `+5 VDC`; 4 `N.C.`; 5 `GROUND`; 6 `-100 VDC`.

## Display connector pin tables (PDF page 53, same foldout; printed text)
`4J1/5J1 (PLAYER 1)` and `4J3/5J3 (PLAYER 3)`: 1 100,000's; 2 -100V KEEP ALIVE; 3 1,000,000's; 4 f SEGMENT; 5 N/C; 6 g SEGMENT;
7 +100V (N/C); 8 e SEGMENT; 9 10,000's; 10 d SEGMENT; 11 1,000's; 12 +100V KEEP ALIVE; 13 100's; 14 COMMA; 15 10's; 16 c SEGMENT;
17 N/C; 18 b SEGMENT; 19 UNITS; 20 a SEGMENT.
`4J2/5J2 (PLAYER 2)` and `4J4/5J4 (PLAYER 4)`: same list with the segments primed: 4 f' SEGMENT; 6 g' SEGMENT; 8 e' SEGMENT; 10 d' SEGMENT;
16 c' SEGMENT; 18 b' SEGMENT; 20 a' SEGMENT (all other pins as above).
`4J8/5J5 (CREDIT/MATCH)`: 1 f' Segment (Credit); 2 -100V Keep Alive; 3 e' Segment; 4 g' Segment; 5 c' Segment; 6 d' Segment;
7 b' Segment; 8 10's; 9 Units; 10 a' Segment (pins 3-10 braced `Credit`); 11 e Segment; 12 f Segment; 13 10's; 14 d Segment (braced
`Match`); 15 +100V Keep Alive; 16 c Segment; 17 g Segment; 18 b Segment; 19 Units; 20 a Segment (pins 16-20 braced `Match`).
Display drawings: `PLAYERS #1 & #3` (seven digits, strobes 2-8, comma marks drawn after the first and fourth digits; connector `5J1` / `5J3`);
`PLAYERS #2 & #4` (seven digits, strobes 10-16; connector `5J2` / `5J4`); `CREDITS / BALL IN PLAY` (four digits, strobe labels `1`, `9`, `1`, `9`;
connector `5J5`). `DETAIL A` `4J1 - 4J4, 4J8 / 5J1 - 5J5 CONNECTORS`: 20-pin (2 x 10) connector sketch, pin 20 and 19 at the top, 2 and 1 at the bottom, `PIN 1 RED LEAD` pointing at the bottom-right pin.

## Observations
- `9B1` is drawn as two lamps in parallel under one designator (`SHOOT AGAIN`).
- Designator prefix is `9` (`9B1`-`9B8`, `9D1`-`9D8`, `9F1`, `9P1`), not `8`; the playfield lamp-sheet bulb list numbers these functions `01`-`08`.
- Missing position: `ROW 7` (9P1 pin 14), `9B7` and `9D7` are not drawn; the printed legends on this sheet are `SHOOT AGAIN` (row 1), `BALL "IN PLAY"` (2),
  `TILT` (3), `GAME OVER` (4), `MATCH` (5), `HIGH SCORE` (6), `BONUS BALL TIMER` (8), compared with the playfield sheet's list
  `01 Same Player Shoots Again (Backbox)`, `02 Ball in Play`, `03 Tilt`, `04 Game Over`, `05 Match`, `06 High Score to Date`,
  `07 Credits (Playfield)`, `08 Bonus Ball Timer`.
- Only one column (`COLUMN 1`, pin 7) is drawn; the 9P1 bar prints no pin numbers 3, 6 or 14.
- The two dashed lamps and the dashed/dotted continuation of the 6.3 V.A.C. lines run off the right end of the drawing.

## Illegible / uncertain items
None unreadable. The caption's printed page number `17` is read from PDF page 55; on PDF page 54 the caption is cut off at the page edge.
