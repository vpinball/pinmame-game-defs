# The Sopranos — Lamp Matrix Grid

Transcribed from `Stern_2005_The_Sopranos_Service_Manual.pdf`, PDF page 7, the front-matter drawing printed `DR. 5`
("LAMP MATRIX GRID & LOCATIONS"), upper half: the 8-column by 10-row lamp matrix. The page is born-digital; the
cell text was taken from the PDF text layer and every cell was checked against a 220 dpi render. The location
drawing and the back-panel inset in the lower half are transcribed in `lamp-locations.md`.

Each cell prints, on its top line, the lamp number in a small box and the bulb (`#555 Clear Bulb`, `#44 Clear Bulb`,
`#44 LED Bulb`, `#555 Yel. Bulb`); below it the lamp name, in black, sometimes with a second line in grey type that
locates the lamp (for example `LEFT OUTLANE` under `( F ) ISH`). Here the black name is given first and the grey line
after a ` / `. Names are otherwise literal, including the parenthesised letters and the `( $ )` marks. Every lamp
number box from 1 to 80 is printed black (the legend's `= Lamps below Playfield.` mark); the 79 cell is shaded grey
(`= Lamps not on Playfield.`). Cells 73-77 carry a small vertical `DOTS` tag (Diode On Terminal Strip).

## Drive columns (18v)

| Column | Driver | Drive wire | Connector |
| --- | --- | --- | --- |
| 1 | U17 | YEL-BRN | J13-P9 |
| 2 | U16 | YEL-RED | J13-P8 |
| 3 | U15 | YEL-ORG | J13-P7 |
| 4 | U14 | YEL-BLK | J13-P6 |
| 5 | U13 | YEL-GRN | J13-P5 |
| 6 | U12 | YEL-BLU | J13-P4 |
| 7 | U11 | YEL-VIO | J13-P3 |
| 8 | U10 | YEL-GRY | J13-P1 |

## Return rows (ground)

| Row | Transistor | Return wire | Connector |
| --- | --- | --- | --- |
| 1 | Q33 | RED-BRN | J12-P1 |
| 2 | Q34 | RED-BLK | J12-P2 |
| 3 | Q35 | RED-ORG | J12-P3 |
| 4 | Q36 | RED-YEL | J12-P4 |
| 5 | Q37 | RED-GRN | J12-P5 |
| 6 | Q38 | RED-BLU | J12-P6 |
| 7 | Q39 | RED-VIO | J12-P8 |
| 8 | Q40 | RED-GRY | J12-P9 |
| 9 | Q41 | RED-WHT | J12-P10 |
| 10 | Q42 | RED | J12-P11 |

## Cells

Lamp number = (row - 1) x 8 + column.

| Lamp | Row / column | Bulb | Name as printed |
| --- | --- | --- | --- |
| 1 | 1 / 1 | #555 Clear Bulb | ( RANKS ) ASSOCIATE |
| 2 | 1 / 2 | #555 Clear Bulb | ( RANKS ) SOLDIER |
| 3 | 1 / 3 | #555 Clear Bulb | ( RANKS ) GOOD EARNER |
| 4 | 1 / 4 | #555 Clear Bulb | ( RANKS ) ACTING CAPO |
| 5 | 1 / 5 | #555 Clear Bulb | ( RANKS ) CAPO |
| 6 | 1 / 6 | #555 Clear Bulb | ( RANKS ) CONSIGLIERE |
| 7 | 1 / 7 | #555 Clear Bulb | ( RANKS ) UNDER BOSS |
| 8 | 1 / 8 | #44 Clear Bulb | ( RANKS ) BOSS |
| 9 | 2 / 1 | #44 Clear Bulb | BOSS: FOOD |
| 10 | 2 / 2 | #44 Clear Bulb | BOSS: TRUCK HEIST |
| 11 | 2 / 3 | #44 Clear Bulb | BOSS: BADA BING |
| 12 | 2 / 4 | #44 Clear Bulb | BOSS: EPISODES |
| 13 | 2 / 5 | #44 Clear Bulb | BOSS: SAFE |
| 14 | 2 / 6 | #44 Clear Bulb | BOSS: RIP |
| 15 | 2 / 7 | #44 Clear Bulb | BOSS: SUPER JACKPOT |
| 16 | 2 / 8 | #44 Clear Bulb | BOSS: MEADOWLANDS |
| 17 | 3 / 1 | #555 Clear Bulb | ( F ) ISH / LEFT OUTLANE |
| 18 | 3 / 2 | #555 Clear Bulb | F ( I ) SH / LT RTRN LANE |
| 19 | 3 / 3 | #555 Clear Bulb | FI ( S ) H / RT RTRN LANE |
| 20 | 3 / 4 | #555 Clear Bulb | FIS ( H ) / RIGHT OUTLANE |
| 21 | 3 / 5 | #555 Clear Bulb | PORK STORE STANDUP |
| 22 | 3 / 6 | #555 Clear Bulb | LIGHT STANDUP |
| 23 | 3 / 7 | #555 Clear Bulb | FISH |
| 24 | 3 / 8 | #44 LED Bulb | THE STUGOTS |
| 25 | 4 / 1 | #555 Clear Bulb | LEFT TRUCK / HEIST 1 ( BOT ) |
| 26 | 4 / 2 | #555 Clear Bulb | LEFT TRUCK / HEIST 2 |
| 27 | 4 / 3 | #555 Clear Bulb | LEFT TRUCK / HEIST 3 |
| 28 | 4 / 4 | #555 Clear Bulb | L. ORBIT FOOD |
| 29 | 4 / 5 | #555 Clear Bulb | L. ORBIT ( $ ) ENVELOPE |
| 30 | 4 / 6 | #555 Clear Bulb | LEFT ORBIT ARROW |
| 31 | 4 / 7 | #555 Clear Bulb | BADA BING 1 (BOT) |
| 32 | 4 / 8 | #555 Clear Bulb | BADA BING 2 |
| 33 | 5 / 1 | #555 Clear Bulb | BADA BING 3 |
| 34 | 5 / 2 | #555 Clear Bulb | L. RAMP FOOD |
| 35 | 5 / 3 | #555 Clear Bulb | L. RAMP ( $ ) ENVELOPE |
| 36 | 5 / 4 | #555 Clear Bulb | LEFT RAMP ARROW |
| 37 | 5 / 5 | #555 Clear Bulb | START EPISODE |
| 38 | 5 / 6 | #555 Clear Bulb | PORK STORE |
| 39 | 5 / 7 | #555 Clear Bulb | SPECIAL |
| 40 | 5 / 8 | #555 Clear Bulb | EXTRA BALL |
| 41 | 6 / 1 | #555 Clear Bulb | ADVANCE RANK |
| 42 | 6 / 2 | #555 Clear Bulb | CENTER ARROW |
| 43 | 6 / 3 | #555 Clear Bulb | LIGHT LOCK |
| 44 | 6 / 4 | #555 Clear Bulb | LOCK 1 |
| 45 | 6 / 5 | #555 Clear Bulb | LOCK 2 |
| 46 | 6 / 6 | #555 Clear Bulb | JACKPOT |
| 47 | 6 / 7 | #555 Clear Bulb | MEADOWLANDS 1 |
| 48 | 6 / 8 | #555 Clear Bulb | MEADOWLANDS 2 |
| 49 | 7 / 1 | #555 Clear Bulb | MEADOWLANDS 3 |
| 50 | 7 / 2 | #555 Clear Bulb | R. RAMP FOOD |
| 51 | 7 / 3 | #555 Clear Bulb | R. RAMP ( $ ) ENVELOPE |
| 52 | 7 / 4 | #555 Clear Bulb | RIGHT RAMP ARROW |
| 53 | 7 / 5 | #555 Clear Bulb | RIGHT TRUCK / HEIST 1 ( BOT ) |
| 54 | 7 / 6 | #555 Clear Bulb | RIGHT TRUCK / HEIST 2 |
| 55 | 7 / 7 | #555 Clear Bulb | RIGHT TRUCK / HEIST 3 |
| 56 | 7 / 8 | #555 Clear Bulb | R. ORBIT FOOD |
| 57 | 8 / 1 | #555 Clear Bulb | R. ORBIT ( $ ) ENVELOPE |
| 58 | 8 / 2 | #555 Clear Bulb | RIGHT ORBIT ARROW |
| 59 | 8 / 3 | #555 Clear Bulb | ( R. ) I. P. / LEFT TOP LANE |
| 60 | 8 / 4 | #555 Clear Bulb | R. ( I. ) P. / MID. TOP LANE |
| 61 | 8 / 5 | #555 Clear Bulb | R. I. ( P. ) / RT. TOP LANE |
| 62 | 8 / 6 | (none) | NOT USED |
| 63 | 8 / 7 | (none) | NOT USED |
| 64 | 8 / 8 | (none) | NOT USED |
| 65 | 9 / 1 | #44 Clear Bulb | RIP 1 ( TOP LEFT) |
| 66 | 9 / 2 | #44 Clear Bulb | RIP 2 |
| 67 | 9 / 3 | #44 Clear Bulb | RIP 3 |
| 68 | 9 / 4 | #44 Clear Bulb | RIP 4 |
| 69 | 9 / 5 | #44 Clear Bulb | RIP 5 ( BOT LEFT ) |
| 70 | 9 / 6 | #44 Clear Bulb | RIP 6 |
| 71 | 9 / 7 | #44 Clear Bulb | RIP 7 |
| 72 | 9 / 8 | #44 Clear Bulb | RIP 8 |
| 73 | 10 / 1 | #555 Yel. Bulb | EPISODES: / ARSON |
| 74 | 10 / 2 | #555 Yel. Bulb | EPISODES: / EXTERMINATE |
| 75 | 10 / 3 | #555 Yel. Bulb | EPISODES: / HORSE RACE |
| 76 | 10 / 4 | #555 Yel. Bulb | EPISODES: / EXEC. GAME |
| 77 | 10 / 5 | #555 Yel. Bulb | EPISODES: / SATISFACTI0N |
| 78 | 10 / 6 | #555 Clear Bulb | SHOOT AGAIN |
| 79 | 10 / 7 | OPTIONAL | TOURNAMENT BUTTON |
| 80 | 10 / 8 | #555 Clear Bulb | START BUTTON |

Cells 62-64 are printed as black blocks reading `NOT USED` with a grey number box. In cell 77 the text layer and the
render both spell `SATISFACTI0N` with a zero; it is kept literally. Cell 79 prints `OPTIONAL` in italics in the bulb
position and `TOURNAMENT BUTTON` in grey italics.

## Notes printed below the drawing

- `Lamp Part Notes: #555 Wedge Base Bulb Clear = 165-5002-00. #555 Wedge Base Bulb Yellow = 165-5054-06 #44 Bayonet Bulb Clear = 165-5000-44. See Section 4, Chapter 1, Parts Identification & Location, Pages 78-80 for more details on bulbs and corresponding sockets.`
- `Lamps 65 thru 72 are located on the rear of the Back Panel.`
- `Some Lamp Diodes may be located under the playfield, in the Cabinet or Backbox on Terminal Strips and not on or with the Lamp Socket. DOTS: Diode On Terminal Strip, see Sec. 5, Chapter 2, Playfield Wiring.`

## Other copies

The grid is reprinted on PDF page 36 (Lamp Test section) and PDF page 214 (inside back cover); those are copies of one
table, not independent sources.
