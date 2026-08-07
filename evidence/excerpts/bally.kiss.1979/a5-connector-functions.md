# Kiss — Lamp Driver A5 connector functions

Transcribed from `Bally_1979_Kiss_Manual.pdf`, PDF page 52, the plug-connector harness sheet, block
headed `LAMP DRIVER A5`. Wire numbers are the small figures to the left of each pin.

The whole block is transcribed rather than only the pins cited, so an unclaimed pin is visible.
`J1` and `J3` are marked **TO PLAYFIELD**; `J2` is marked **TO BACKBOX**, though Table B on the same
sheet routes seven J2 pins onward to playfield inserts through the panel-to-back-cab plug.

## J1 — to playfield

| pin | wire | function |
| --- | --- | --- |
| 1 | 41 | Red "I" |
| 2 | 43 | White Arrow |
| 3 | 45 | Green "I" |
| 4 | 35 | N/U |
| 5 | 48 | "I" Rollover |
| 6 | 25 | "B" Target |
| 7 | 34 | White Kiss Amber Arrow |
| 8 | 51 | Yellow "I" |
| 9 | 52 | White "I" |
| 10 | 32 | "I" Amber Arrow |
| 11 | 65 | Top & Bottom Thumper Bumper |
| 12 | 61 | Left Spinner |
| 13 | 96 | "C" Target |
| 14 | 54 | Red Arrow |
| 15 | 13 | "K" Amber Arrow |
| 16 | 12 | Red Kiss Amber Arrow |
| 17 | 25 | Yellow "K" |
| 18 | 57 | Red "K" |
| 19 | 60 | White "K" |
| 20 | — | KEY |
| 21 | — | N/U |
| 22 | — | N/U |
| 23 | 56 | Green "K" |
| 24 | 50 | "K" Rollover |
| 25 | 90 | A-B-C-D Target Extra Ball |
| 26 | 91 | N/U |
| 27 | 53 | Right Spinner |
| 28 | 78 | "A" Target |

## J2 — to backbox

| pin | wire | function |
| --- | --- | --- |
| 1 | 60 | 2X Bonus |
| 2 | 20 | Kiss Special |
| 3 | 84 | N/U |
| 4 | 72 | N/U |
| 5 | — | N/U |
| 6 | 85 | Open Gate W/L |
| 7 | 91 | A-B-C-D Special |
| 8 | 93 | Match |
| 9 | — | N/U |
| 10 | 98 | Tilt |
| 11 | 95 | Game Over |
| 12 | 61 | N/U |
| 13 | 53 | N/U |
| 14 | 12 | 40,000 Bonus |
| 15 | 32 | 80,000 Colossal |
| 16 | 34 | N/U |
| 17 | — | N/U |
| 18 | — | KEY |
| 19 | — | N/U |
| 20 | 35 | Light A Line W/L |
| 21 | 47 | Shoot Again |
| 22 | 62 | Ball In Play |
| 23 | 97 | High Score To Date |

## J3 — to playfield

| pin | wire | function |
| --- | --- | --- |
| 1 | 10 | Red "S" (Right) |
| 2 | 95 | "D" Target |
| 3 | 81 | Right "S" Amber Arrow |
| 4 | 14 | Green Kiss Amber Arrow |
| 5 | — | N/U |
| 6 | — | N/U |
| 7 | — | N/U |
| 8 | — | KEY |
| 9 | 15 | Green Arrow |
| 10 | 91 | "S" Outer Rollover |
| 11 | 20 | Green "S" (Right) |
| 12 | 21 | White "S" (Right) |
| 13 | 12 | Credit Indicator |
| 14 | 84 | Left Out Special |
| 15 | 53 | Yellow "S" (Right) |
| 16 | 25 | Yellow Arrow |
| 17 | 27 | Green "S" (Left) |
| 18 | 56 | A-B-C-D Target 2X |
| 19 | 67 | Yellow "S" (Left) |
| 20 | 64 | Left & Right Thumper Bumper |
| 21 | 30 | "S" Inner Rollover |
| 22 | 23 | Same Player Shoots Again |
| 23 | 22 | Left "S" Amber Arrow |
| 24 | 98 | Right Out Special |
| 25 | 36 | White "S" (Left) |
| 26 | 38 | Red "S" (Left) |
| 27 | 40 | Yellow Kiss Amber Arrow |
| 28 | — | N/U |

## Table B — panel to back cab. plug

The same sheet routes these A5J2 pins onward, so each lights a backglass socket *and* a playfield
insert. This is why seven J2 addresses carry a playfield coordinate.

| from | to pin | wire |
| --- | --- | --- |
| A5J2-14 | 1 | 12 |
| A5J2-2 | 2 | 20 |
| A5J2-15 | 3 | 32 |
| A5J2-20 | 4 | 35 |
| A5J2-1 | 5 | 60 |
| A5J2-6 | 6 | 85 |
| A5J2-7 | 7 | 91 |
| A2J1-7 | 8 | 20 |

## Why the whole block matters

An earlier pass read one connector endpoint per SCR and carried Centaur's endpoint list over to
Kiss. That dropped eight real lamp sockets, because the AS-2518-23 fans several SCRs out to two
branches and each game's harness plugs a different one. `J3-22 Same Player Shoots Again` above is
the clearest case: its SCR Q40 also reaches `J2-9`, which is N/U, and only the J2 branch is unused.
Transcribing the whole block rather than the rows already believed relevant is what makes an
unclaimed pin visible.
