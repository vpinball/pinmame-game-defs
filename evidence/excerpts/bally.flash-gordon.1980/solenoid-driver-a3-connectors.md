# Flash Gordon - Solenoid Driver A3 connectors, Tables B and C, Strobe Module A13

Transcribed from `Flash Gordon Bally 1981 English Manual.pdf`, PDF page 49, drawing `W-1187-26C`,
titled `WIRING DIAGRAM BACK BOX`, material code `FLASH GORDON`, game `#1215`, drawn 11-16-80. Read
from a 200 dpi `pdftoppm` render.

`A3` is the Voltage Regulator / Solenoid Driver module. Its output-side connector blocks are
transcribed whole. **These pin numbers are not the public solenoid addresses**; nothing in this
definition derives an address from them.

## A3 J1 (9 pins)

| Wire | Pin | To |
| --- | --- | --- |
| - | 1 | N/U |
| 18 | 2 | 3 D.T. RESET |
| 67 | 3 | 4 D.T. RESET |
| - | 4 | N/U |
| 95 | 5 | OUTHOLE |
| - | 6 | N/U |
| - | 7 | KEY |
| 40 | 8 | L FLIP COIL |
| 70 | 9 | R FLIP COIL |

## A3 J2 (12 pins)

| Wire | Pin | To |
| --- | --- | --- |
| C | 1 | R FLIP SW |
| 20 | 2 | L FLIP SW |
| - | 3 | KEY |
| - | 4 | N/U |
| 85 | 5 | KNOCKER |
| - | 6 | NOTE 1 |
| 31 | 7 | TEST SW RET |
| 36 | 8 | COIN LOCKOUT |
| 58 | 9 | NOTE 1 |
| 81 | 10 | IN-LINE DROP TAR. RESET |
| 75 | 11 | SAUCER KICK-DN. |
| 54 | 12 | N/U |

## A3 J5 (15 pins)

| Wire | Pin | To |
| --- | --- | --- |
| - | 1 | N/U |
| - | 2 | N/U |
| - | 3 | N/U |
| - | 4 | N/U |
| - | 5 | N/U |
| - | 6 | KEY |
| 81 | 7 | N/U |
| 18 | 8 | RIGHT SLINGSHOT |
| 71 | 9 | R.T. THUMPER BUMPER |
| 85 | 10 | SAUCER KICK-UP |
| 78 | 11 | LEFT THUMPER BUMPER |
| 80 | 12 | SINGLE D.T. RESET |
| 67 | 13 | TOP THUMPER BUMPER |
| 83 | 14 | LEFT SLINGSHOT |
| 74 | 15 | SINGLE D.T. PULL DOWN |

Across J1, J2 and J5 the sheet names fourteen distinct coil destinations - outhole, knocker, coin
lockout, saucer kick-up, saucer kick-down, single drop target reset, single drop target pull down,
3 drop target reset, 4 drop target reset, in-line drop target reset, left/right/top thumper bumper,
left and right slingshot - plus the two flipper-coil feeds. That is fourteen driver-board coil
destinations for the fifteen momentary outputs the platform publishes.

The two flipper feeds are the only flipper-coil connections anywhere on the board, so a machine
with more flipper coils than feeds parallels them onto one feed. The coil count itself is in the
parts list; see `parts-list-coils.md`.

## Table B - PANEL TO BACK CAB. PLUG

| From | Pin | Wire |
| --- | --- | --- |
| A5J2-14 | 1 | 12 |
| A5J2-2 | 2 | 20 |
| A5J2-15 | 3 | 23 |
| A5J2-16 | 4 | 34 |
| A5J2-1 | 5 | 60 |
| A5J2-6 | 6 | 85 |
| A5J2-7 | 7 | 91 |
| A5J2-20 | 8 | 98 |

Eight rows. Each wire colour matches the code the A5 J2 column prints against the same pin, so the
two sheets agree. These eight A5J2 circuits are carried onward from the back box insert panel to
playfield inserts; the other six functional A5J2 pins are the insert-panel lamps themselves.

## Table C - T2 TO STROBE MODULE

| From | Pin | Wire |
| --- | --- | --- |
| A2J | AJ2 | 40 |
| AJJ | AJ4 | 70 |

## Strobe Module A13 (J1, 8 pins)

| Wire | Pin | To |
| --- | --- | --- |
| 40 | 1 | 115 VAC |
| - | 2 | N/U |
| 70 | 3 | 115 VAC |
| - | 4 | N/U |
| - | 5 | KEY |
| - | 6 | N/U |
| 72 | 7 | A9J3-18 |
| 20 | 8 | SW. ILL. |

A13 pin 7 is fed from A9J3-18, the auxiliary lamp driver circuit printed `BACK BOX STROBE`. The
strobe module is the back box flash tube assembly `AS-2518-62` (PDF page 36), not a playfield device.

## Solid State Sound System Module A8 and general illumination

The same sheet draws `SOLID STATE SOUND SYSTEM MODULE A8` with its own J1/J2, and two
`GEN ILL. LAMPS` circuits driven from `5.9 V.A.C.` off the transformer via A2J4-8 / A2J4-1 and
A2J4-9 / A2J4-4. General illumination has no connection to any driver board on this machine.
