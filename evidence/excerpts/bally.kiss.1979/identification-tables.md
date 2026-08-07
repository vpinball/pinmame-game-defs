# Kiss — solenoid and switch identification tables

Transcribed from `Bally_1979_Kiss_Manual.pdf`, PDF page 22, both identification tables, read from
the rendered page rather than the text layer.

## Solenoid identification

The left column is the **Self Test #**, which is a test *order*, not a controller address. Page 21
of the same manual says so implicitly: pressing the self-test switch three times enters the solenoid
test, and "a number is flashed on the Player Score displays as each solenoid is pulsed". The public
address column was read off the running ROM by pairing each pulsed address with that displayed
number, and it repeated identically across five complete cycles.

| Self Test # | printed name | public address |
| --- | --- | --- |
| 01 | Outhole Kicker | 7 |
| 02 | Knocker | 6 |
| 03 | Drop Target Reset | 14 |
| 04 | Left Thumper Bumper | 9 |
| 05 | Right Thumper Bumper | 10 |
| 06 | Bottom Thumper Bumper | 11 |
| 07 | Top Thumper Bumper | 8 |
| 08 | Left Slingshot | 12 |
| 09 | Right Slingshot | 13 |
| 10 | Right Bottom Gate | 17 |
| 11 | Coin Lockout Door | 18 |
| 12 | K1 Relay (Flipper Enable) | 19 |

Page 23 annotates the same numbers with their location: `DOOR: 11`, `BACK BOX: 12`, `CABINET: 02`.

No printed number equals its public address, which is the point: the two columns are unrelated.

## Switch identification

Forty switches in five columns. Blank entries are blank on the printed page. Bracketed figures are
the number of physical contacts wired in parallel onto one address.

| # | function | | # | function |
| --- | --- | --- | --- | --- |
| 01 | Drop Target D (Bottom) | | 21 | Outer "S" Rollover |
| 02 | Drop Target C | | 22 | Inner "S" Rollover |
| 03 | Drop Target B | | 23 | "I" Rollover |
| 04 | Drop Target A (Top) | | 24 | "K" Rollover |
| 05 | Lite-A-Line 5,000 Rollover | | 25 | Drop Target and 2 Rebs. (3) |
| 06 | Credit Button | | 26 | Right Flip/Feed Lane |
| 07 | Tilt (3) | | 27 | Left Flip/Feed Lane |
| 08 | Outhole | | 28 | *(blank)* |
| 09 | Coin III (Right) | | 29 | *(blank)* |
| 10 | Coin I (Left) | | 30 | Right Spinner |
| 11 | Coin II (Middle) | | 31 | Left Spinner |
| 12 | "D" Target | | 32 | *(blank)* |
| 13 | "C" Target | | 33 | Right Outlane |
| 14 | "B" Target | | 34 | Left Outlane |
| 15 | "A" Target | | 35 | Right Slingshot |
| 16 | Slam (2) | | 36 | Left Slingshot |
| 17 | Lower "S" Target | | 37 | Bottom Thumper Bumper |
| 18 | Upper "S" Target | | 38 | Top Thumper Bumper |
| 19 | "I" Target | | 39 | Right Thumper Bumper |
| 20 | "K" Target | | 40 | Left Thumper Bumper |

Printed note beneath the table:

> SLINGSHOT AND THUMPER BUMPER COILS WILL ENERGIZE WHEN SWITCH IS MADE.

That sentence is the authority for the six `direct` switch-to-coil relationships in the definition:
those coils fire from their own switch rather than waiting for the ROM, and a recreation must
reproduce that immediacy.
