# Flash Gordon - Switch Matrix (Playfield A6 schematic)

Transcribed from `Flash Gordon Bally 1981 English Manual.pdf`, PDF page 46, sheet headed
`PLAYFIELD A6` of drawing `W-1187-26`, read from a 400 dpi `pdftoppm` render. The accompanying crop
is the same matrix block, grayscale, so a reader can confirm the negative claim about optos below
without holding the document.

Five strobe columns and eight return lines, so forty matrix positions and no more:

| Strobe | MPU pin | Wire |
| --- | --- | --- |
| ST 0 | A4J2-1 | 51 |
| ST 1 | A4J2-2 | 70 |
| ST 2 | A4J2-3 | 93 |
| ST 3 | A4J2-4 | 53 |
| ST 4 | A4J2-5 | 31 |

| Return | MPU pin | Wire |
| --- | --- | --- |
| I 0 | A4J2-8 | 54 |
| I 1 | A4J2-9 | 63 |
| I 2 | A4J2-10 | 57 |
| I 3 | A4J2-11 | 78 |
| I 4 | A4J2-12 | 60 |
| I 5 | A4J2-13 | 56 |
| I 6 | A4J2-14 | 65 |
| I 7 | A4J2-15 | 52 |

There is no ST 5 stub anywhere on the sheet, which is what makes Flash Gordon a five-column game.
Sheet notes printed at the bottom: `1. INDICATES NOT USED`, `2. N/U = NOT USED ON PLAYFIELD`,
`3. * INDICATES AID TEST POINT`, `4. COIL DIODES ARE 1N4004 (E-587-6); ALL CAPACITORS ARE .05 MFD
(E-586-80); SWITCH DIODES ARE 1N4148 (E-587-14)`, `5. GERMANY ONLY - CAPACITOR .01 MFD @ 500 V
(E-586-65)`.

Every drawn switch is an ordinary mechanical contact in series with a 1N4148 diode, some with a
.05 MFD capacitor across them. **No cell on this sheet is drawn as, or annotated as, an opto
interrupter, and the sheet carries no opto legend of any kind.** Nothing on this machine's switch
matrix is opto-constructed; it is a 1980 machine whose forty positions are rollover buttons, leaf
contacts, drop-target and standup-target contacts, spinner contacts and cabinet contacts.

Public address = (column - 1) * 8 + row + 1, with column ST0..ST4 = 1..5 and row I0..I7 = 0..7.

| Public | Column/row | Printed label on this sheet |
| --- | --- | --- |
| 1 | ST0 I0 | 2 LEFT AND RIGHT ROLLOVER BUTTONS |
| 2 | ST0 I1 | 3 SHOOTER LANE ROLLOVER BUTTONS |
| 3 | ST0 I2 | SINGLE DROP TARGET |
| 4 | ST0 I3 | SHOOTER LANE ROLLOVER |
| 5 | ST0 I4 | DROP TARGETS 50 POINT REBOUND (2) |
| 6 | ST0 I5 | *(switch drawn, no label - not used on playfield)* |
| 7 | ST0 I6 | TILT |
| 8 | ST0 I7 | OUTHOLE |
| 9 | ST1 I0 | *(switch drawn, no label - not used on playfield)* |
| 10 | ST1 I1 | *(switch drawn, no label - not used on playfield)* |
| 11 | ST1 I2 | *(switch drawn, no label - not used on playfield)* |
| 12 | ST1 I3 | RIGHT SIDE UPPER TARGET |
| 13 | ST1 I4 | FLIPPER FEED LANE (RIGHT) |
| 14 | ST1 I5 | FLIPPER FEED LANE (LEFT) |
| 15 | ST1 I6 | RIGHT SIDE LOWER TARGET |
| 16 | ST1 I7 | *(switch drawn, no label - not used on playfield)* |
| 17 | ST2 I0 | 4 DROP TARGET "A" (BOTTOM) |
| 18 | ST2 I1 | 4 DROP TARGET "B" |
| 19 | ST2 I2 | 4 DROP TARGET "C" |
| 20 | ST2 I3 | 4 DROP TARGET "D" (TOP) |
| 21 | ST2 I4 | 3 DROP TARGET (TOP) |
| 22 | ST2 I5 | 3 DROP TARGET (MIDDLE) |
| 23 | ST2 I6 | 3 DROP TARGET (BOTTOM) |
| 24 | ST2 I7 | TOP TARGET |
| 25 | ST3 I0 | 1ST IN LINE DROP TARGET |
| 26 | ST3 I1 | 2ND IN LINE DROP TARGET |
| 27 | ST3 I2 | 3RD IN LINE DROP TARGET |
| 28 | ST3 I3 | IN LINE BACK TARGET |
| 29 | ST3 I4 | 10 POINT REBOUND (2) |
| 30 | ST3 I5 | SAUCER |
| 31 | ST3 I6 | RIGHT OUTLANE |
| 32 | ST3 I7 | LEFT OUTLANE |
| 33 | ST4 I0 | RIGHT SPINNER |
| 34 | ST4 I1 | LEFT SPINNER |
| 35 | ST4 I2 | RIGHT SLINGSHOT |
| 36 | ST4 I3 | LEFT SLINGSHOT |
| 37 | ST4 I4 | TOP THUMPER BUMPER |
| 38 | ST4 I5 | *(switch position drawn, no label)* |
| 39 | ST4 I6 | RIGHT THUMPER BUMPER |
| 40 | ST4 I7 | LEFT THUMPER BUMPER |

Every label above matches the printed Switch Assembly Self-Test Display Numbers table row for row
**except public 12 and 15**, which this sheet prints as UPPER and LOWER respectively while the
self-test table prints them as LOWER and UPPER. See `figure-v-locations.md`.

## Playfield coils drawn on the same sheet

The right-hand half of the sheet draws the playfield solenoid coils in pairs with their A3 connector
pins, each with a 1N4004 across it:

| Coil pair | Connector pins |
| --- | --- |
| LEFT FLIPPER / RIGHT FLIPPER | A3J1-8 (wire 40), A3J1-9 (wire 70), A3J1-5 (wire 95), +43 VDC from A2J1-6 (wire 60) |
| SAUCER KICK UP / LEFT THUMPER BUMPER | A3J5-10 (wire 85), A3J5-11 (wire 78), A3J5-12 (wire 80) |
| RIGHT THUMPER BUMPER / SINGLE DROP TARGET PULL DOWN | A3J5-9 (wire 71), A3J5-15 (wire 74), A3J5-13 (wire 67) |
| LEFT SLINGSHOT / RIGHT SLINGSHOT | A3J5-14 (wire 83), A3J5-8 (wire 18) |
| IN LINE DROP TARGET RESET / SAUCER KICK DOWN | A3J2-10 (wire 81), A3J2-11 (wire 80) |
| 3 DROP TARGET RESET / 4 DROP TARGET RESET | A3J1-2 (wire 18), A3J1-3 (wire 67) |

General illumination is drawn on this same sheet as a plain transformer circuit - `5.9 VAC`,
`GEN. ILLUM.`, wires 10/70 to A2J1-8/A2J1-5 and wires 40/50 to A2J1-2/A2J1-1 with a return. It has
no driver-board output and no controller address of any kind.
