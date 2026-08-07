# Big Bang Bar — Solenoids, Motors, & Flashers (manual location table)

Transcribed from `Capcom_1996_Big_Bang_Bar_Manual.pdf`, printed page 82 (PDF page 86),
"SOLENOIDS, MOTORS, & FLASHERS". Rendered at 250-300 dpi, read visually. Single-page table
plus a numbered playfield-location diagram on the same page; no wire colors or opto data on
this page, only `Ref.`, `Description`, and `Part Number`. PDF page number = printed page
number + 4.

| Ref. | Description | Part Number |
| --- | --- | --- |
| 1 | OUTHOLE | CL00109 |
| 2 | TROUGH | CL00109 |
| 3 | KNOCKER | CL00109 |
| 4 | LEFT SLINGSHOT | CL00109 |
| 5 | RIGHT SLINGSHOT | CL00109 |
| 6 | KICKBACK | CL00109 |
| 7 | 4-BANK RESET | CL00109 |
| 8 | LOWER LOCK POST | CL00109 |
| 9 | LEFT FLIPPER | CL00109 |
| 10 | RIGHT FLIPPER | CL00109 |
| 11 | UPPER RIGHT FLIPPER | CL00109 |
| 12 | EJECT HOLE | CL00109 |
| 13 | ISLAND DIVERTER 1 | CL00112 |
| 14 | RAMP DIVERTER 1 | CL00109 |
| 15 | RAMP DIVERTER 2 | CL00109 |
| 16 | ALIEN LOCK POST | CL00109 |
| 17 | 3-BANK RESET | CL00109 |
| 18 | STAR BUMPER LEFT | CL00109 |
| 19 | STAR BUMPER MIDDLE | CL00109 |
| 20 | STAR BUMPER RIGHT | CL00109 |
| 21 | BACKBOX LEFT (FLASHER) | LP00101 |
| 22 | TUBE DANCER | CL00109 |
| *(blank Ref.)* | BACKBOX RIGHT (FLASHER) | LP00101 |
| 23 | DANCE FLOOR (FLASHER) | LP00101 |
| 24 | EJECT HOLE (FLASHER) | LP00101 |
| 25 | ALIENS (FLASHER) | LP00101 |
| 26 | LOWER LOCK (FLASHER) | LP00101 |
| 27 | ORBIT GATE LEFT | CL00112 |
| 28 | ORBIT GATE RIGHT | CL00112 |
| 29 | 1-BANK RESET | CL00109 |
| 30 | TUBE DANCER (MOTOR) | MR00108 |
| 31 | ALIENS FORWARD (MOTOR) | MR00108 |
| 32 | ALIENS REVERSE (MOTOR) | MR00108 |

The blank-`Ref.` "BACKBOX RIGHT (FLASHER)" row is resolved by the companion schematic sheet
7's own device table (see `solenoid-schematic-device-table.md`): address S22 is named "TUBE
DANCER & B.B. R." — one physical driver address feeding two devices in parallel (the Tube
Dancer effect and the Backbox Right flasher), which is exactly why this table prints two
description rows sharing one Ref/address with only one of them numbered. It is not a
numbering gap.

Part numbers: `CL00109` (generic coil, used for 27 of the 32 rows), `CL00112` (gate/diverter
coil: 13 Island Diverter 1, 27/28 Orbit Gate Left/Right), `LP00101` (dedicated flasher lamp:
21, unnumbered Backbox Right, 23, 24, 25, 26), `MR00108` (motor: 30, 31, 32).
