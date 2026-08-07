# Flash Gordon - Solenoid and Switch Self-Test Tables

Transcribed from `Flash Gordon Bally 1981 English Manual.pdf`, PDF page 22, printed page 17, headed
`GAME #1215 FLASH GORDON (FIGURE V)`. Read from a 300 dpi `pdftoppm` render; the PDF's own OCR text
layer scrambles both two-column tables and was never trusted.

Two separate printed tables live on this page. **Neither column is a controller address.** The
manual itself says so for solenoids: its troubleshooting section (PDF page 21, printed 16, symptom
4A) instructs the operator to press the self-test button three times and states that "a number is
flashed on the Player Score displays as each solenoid is pulsed", which makes the Self Test # a test
*order*. For switches the numbers do turn out to equal the public matrix positions, but that is a
result derived from the Playfield A6 schematic and the retained script, not an assumption.

## Solenoid Identification Table

| Self Test # | Solenoid identification | Self Test # | Solenoid identification |
| --- | --- | --- | --- |
| 01 | OUTHOLE KICKER | 09 | LEFT THUMPER BUMPER |
| 02 | KNOCKER | 10 | RIGHT THUMPER BUMPER |
| 03 | SAUCER KICK DOWN | 11 | SINGLE DROP TARGET PULL DOWN |
| 04 | SAUCER KICK UP | 12 | TOP THUMPER BUMPER |
| 05 | SINGLE DROP TARGET RESET | 13 | LEFT SLINGSHOT |
| 06 | 4 DROP TARGET | 14 | RIGHT SLINGSHOT |
| 07 | 3 DROP TARGET | 15 | COIN LOCKOUT DOOR |
| 08 | IN LINE DROP TARGET | 16 | KI RELAY (FLIPPER ENABLE) |

Sixteen entries, 01 through 16, with no blanks. "KI RELAY" is the printed spelling of K1 Relay.

## Switch Assembly Self-Test Display Numbers

| Self Test # | Description | Self Test # | Description |
| --- | --- | --- | --- |
| 01 | 2 LEFT & RIGHT R.O. BUTTONS | 21 | 1 DROP TARGET (TOP) |
| 02 | 3 SHOOTER LANE R.O. BUTTONS | 22 | 2 DROP TARGET (MIDDLE) |
| 03 | TOP SINGLE DROP TARGET | 23 | 3 DROP TARGET (BOTTOM) |
| 04 | SHOOTER LANE ROLLOVER | 24 | TOP TARGET |
| 05 | DROP TARGET 50 POINT REB. (2) | 25 | 1st INLINE DROP TARGET |
| 06 | CREDIT BUTTON | 26 | 2nd INLINE DROP TARGET |
| 07 | TILT (3) | 27 | 3rd INLINE DROP TARGET |
| 08 | OUTHOLE | 28 | INLINE BACK TARGET |
| 09 | COIN III (RIGHT) | 29 | 10 POINT REBOUND (2) |
| 10 | COIN I (LEFT) | 30 | SAUCER |
| 11 | COIN II (MIDDLE) | 31 | RIGHT OUTLANE |
| 12 | LOWER RIGHT SIDE TARGET | 32 | LEFT OUTLANE |
| 13 | FLIP FEED LANE (RIGHT) | 33 | RIGHT SPINNER |
| 14 | FLIP FEED LANE (LEFT) | 34 | LEFT SPINNER |
| 15 | UPPER RIGHT SIDE TARGET | 35 | RIGHT SLINGSHOT |
| 16 | SLAM (2) | 36 | LEFT SLINGSHOT |
| 17 | 4 DROP TARGET "A" (BOTTOM) | 37 | TOP THUMPER BUMPER |
| 18 | 4 DROP TARGET "B" | 38 | *(printed blank)* |
| 19 | 4 DROP TARGET "C" | 39 | RIGHT THUMPER BUMPER |
| 20 | 4 DROP TARGET "D" (TOP) | 40 | LEFT THUMPER BUMPER |

Forty numbered rows, 01 through 40. Row 38 is the only one printed with no description at all; every
other row carries text. Forty positions is five matrix columns of eight, and the Playfield A6 switch
schematic (see `switch-matrix-schematic.md`) confirms independently that only ST0 through ST4 are
strobed.

Footnote printed below the right-hand column, unscoped and applying to the whole table:

> **NOTE:** SLINGSHOT & THUMPER BUMPER COILS WILL BE ENERGIZED WHEN SWITCH IS MADE

`(2)` and `(3)` in a description are contact counts: switch 05 is two rebound contacts in parallel,
switch 07 is three tilt contacts, switch 16 is two slam contacts, switch 29 is two rebound contacts.

Rows 12 and 15 disagree with the Playfield A6 schematic sheet, which prints the two right-side
standup targets the other way round. See `switch-matrix-schematic.md` and `figure-v-locations.md`.
