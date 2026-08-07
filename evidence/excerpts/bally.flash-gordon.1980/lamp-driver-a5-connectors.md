# Flash Gordon - Lamp Driver A5 connector functions

Transcribed from `Flash Gordon Bally 1981 English Manual.pdf`, PDF page 48, the drawing sheet
carrying `TABLE A`, `A1 INSERT` and the `LAMP DRIVER A5` connector block, read from 400 dpi
`pdftoppm` renders of each connector column in turn. The PDF's own OCR interleaves the four columns
and was not trusted for a single row.

`A5` is the AS-2518-23 Lamp Driver (named in the parts list, PDF page 25). J4 is its input connector
from the MPU and the voltage regulator; J1, J2 and J3 carry the board's sixty lamp outputs. The
sheet draws arrows out of these blocks reading `TO LOWER CABINET` and `TO PLAYFIELD`. Sheet notes:
`1. THESE PINS ARE RESERVED FOR FUTURE USE. 2. WIRE COLOR ARE SHOWN FOR ALL CONNECTOR PINS, SOME
WIRE MAY NOT BE USED IN ALL GAMES. 3. * INDICATES AID TEST POINT.`

The whole of each output column is transcribed, including every `N/U`, `KEY` and blank pin, so an
unclaimed pin is visible here rather than only in whichever rows this definition happened to use.
The leading number in each row is the printed wire-colour code.

## A5 J1 (28 pins)

| Wire | Pin | Function |
| --- | --- | --- |
| 41 | 1 | 2K MINI BONUS |
| 52 | 2 | 6K SUPER BONUS |
| 45 | 3 | 2K SUPER BONUS |
| 35 | 4 | N/U |
| 48 | 5 | 4 DROP TAR. "B" |
| 25 | 6 | #2 DROP TAR. ARW. |
| 34 | 7 | 3X BONUS |
| 51 | 8 | 10K MINI BONUS |
| 43 | 9 | 6K MINI BONUS |
| 23 | 10 | 10K SUPER BONUS |
| 65 | 11 | FLIPPER FEED LANE (RT.) |
| 61 | 12 | 20K SAUCER |
| 96 | 13 | #3 DROP TAR. ARW. |
| 54 | 14 | 5K SUPER BONUS |
| 13 | 15 | 9K SUPER BONUS |
| 90 | 16 | 2X BONUS |
| 57 | 17 | 9K MINI BONUS |
| 58 | 18 | 1K MINI BONUS |
| 60 | 19 | 5K MINI BONUS |
| - | 20 | KEY |
| - | 21 | N/U |
| - | 22 | N/U |
| 12 | 23 | 1K MINI BONUS |
| 50 | 24 | 4 DROP TAR "A" (bottom) |
| 75 | 25 | RT. SIDE LWR TAR. |
| 91 | 26 | N/U |
| 53 | 27 | 10K SAUCER |
| 78 | 28 | #1 DROP TAR. ARW. |

Pin 18 and pin 23 are both printed `1K MINI BONUS`. See `## The duplicate 1K row` below.

## A5 J2 (23 pins)

| Wire | Pin | Function |
| --- | --- | --- |
| 60 | 1 | TOP TAR. SPECIAL |
| 20 | 2 | LOWER TOP RT. R.O. BUTTON |
| 84 | 3 | N/U |
| 72 | 4 | N/U |
| - | 5 | N/U |
| 85 | 6 | 30K SAUCER |
| 91 | 7 | TOP TAR. COL. B'NUS |
| 70 | 8 | MATCH |
| - | 9 | N/U |
| 35 | 10 | TILT |
| 95 | 11 | GAME OVER |
| 61 | 12 | N/U |
| 53 | 13 | N/U |
| 12 | 14 | RT. OUT SPECIAL |
| 23 | 15 | LFT. OUT SPECIAL |
| 34 | 16 | TOP THUM. BUMP. |
| - | 17 | N/U |
| - | 18 | KEY |
| - | 19 | N/U |
| 98 | 20 | IN-LINE DROP TAR. X-BALL |
| 47 | 21 | SHOOT AGAIN |
| 62 | 22 | BALL IN PLAY |
| 97 | 23 | HIGH SCORE TO DATE |

Fourteen J2 pins carry a function. Eight of them (1, 2, 6, 7, 14, 15, 16, 20) reappear in Table B,
the `PANEL TO BACK CAB. PLUG` list on PDF page 49, which carries them onward to playfield inserts.
The six that do not - 8 MATCH, 10 TILT, 11 GAME OVER, 21 SHOOT AGAIN, 22 BALL IN PLAY, 23 HIGH SCORE
TO DATE - are the back box insert-panel lamps.

## A5 J3 (28 pins)

| Wire | Pin | Function |
| --- | --- | --- |
| 10 | 1 | 4K MINI BONUS |
| 95 | 2 | 4X 3 DROP TAR. |
| 81 | 3 | 100K SUPER BONUS |
| 14 | 4 | 5X BONUS |
| - | 5 | N/U |
| - | 6 | N/U |
| - | 7 | N/U |
| - | 8 | KEY |
| 15 | 9 | 8K SUPER BONUS |
| 91 | 10 | 4 DROP TAR. "D" (top) |
| 20 | 11 | 4K SUPER BONUS |
| 21 | 12 | 8K MINI BONUS |
| 35 | 13 | CREDIT INDICATOR |
| 84 | 14 | 5X 4 DROP TAR. |
| 53 | 15 | LEFT SPINNER |
| 25 | 16 | 7K SUPER BONUS |
| 13 | 17 | 3K SUPER BONUS |
| 56 | 18 | RT. SIDE UP'R TAR. |
| 67 | 19 | RT. SPINNER |
| 64 | 20 | FLIPPER FEED LANE (LEFT) |
| 30 | 21 | 4 DROP TAR. "C" |
| 23 | 22 | SAME PLAYER S.A. |
| 98 | 23 | 50K MINI BONUS |
| 72 | 24 | X-BALL SAUCER |
| 36 | 25 | 7K MINI BONUS |
| 43 | 26 | 3K MINI BONUS |
| 40 | 27 | 4X BONUS |
| - | 28 | N/U |

## A5 J4 (17 pins, input side)

| Wire | Pin | To |
| --- | --- | --- |
| 51 | 1 | A2J3-3 |
| 18 | 2 | A2J3-2 |
| 84 | 3 | A3J3-16 |
| 74 | 4 | A4J1-19 |
| 71 | 5 | A4J1-18 |
| 23 | 6 | A4J1-17 |
| 63 | 7 | A4J1-16 |
| - | 8 | KEY |
| - | 9 | N/U |
| - | 10 | N/U |
| 58 | 11 | A2J3-4 |
| - | 12 | SPARE GND |
| 75 | 13 | A4J1-11 |
| 32 | 14 | A4J1-15 |
| 13 | 15 | A4J1-14 |
| 45 | 16 | A4J1-13 |
| 48 | 17 | A4J1-12 |

## The duplicate 1K row

J1-18 and J1-23 are both printed `1K MINI BONUS`, which cannot both be right. Sweeping every
function printed on J1, J2 and J3 for a bonus value gives eleven MINI BONUS steps - 1K, 2K, 3K, 4K,
5K, 6K, 7K, 8K, 9K, 10K and 50K - and ten SUPER BONUS steps - 2K, 3K, 4K, 5K, 6K, 7K, 8K, 9K, 10K
and 100K. The single value missing from the SUPER BONUS ladder is its 1K step, and the single
duplicated row is J1-23. The retained known-working table independently binds the address J1-23
feeds to its own `LBonus1`, and its `LBonusN` names track the SUPER BONUS ladder while its
`LMiniBonusN` names track the MINI BONUS ladder, agreeing address for address on all twenty other
steps. J1-23 is therefore `1K SUPER BONUS` and J1-18 is `1K MINI BONUS`.
