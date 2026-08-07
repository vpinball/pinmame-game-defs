# Batman (Data East 1991) - Coil drivers and the Left/Right relay

Transcribed by hand from a 400 dpi render of printed page 28 and 29 (PDF 32 and 33). This manual has no text
layer at all (70 pages, 0 characters), so nothing here came from `pdftotext`.

The manual's own statement of the multiplexing mechanism, printed page 28:

> Twenty-Two regular (pulsed under microprocessor control) coil drivers are provided to switch ground to coils. The Left/Right relay is used in conjunction with drives 1 through 8 to switch +32 volts between coils or flash lamps; these sets are termed "left" and "right". This relay is located on the PPB board which provides isolation diodes and current limiting resistors. This effectively provides 29 regular coils.

## Drives 1-8, switched between a left and a right set by the relay

| Drive | Transistor | Wire | Left (coil) | Coil type | Right (flash lamps) |
| --- | --- | --- | --- | --- | --- |
| 1 | Q46 | GRY-BRN CN-11 | Outhole | 23-840 | (4) No. 89 (3 playfield, 1 insert) |
| 2 | Q45 | GRY-RED CN-11 | Trough Eject | 23-840 | (3) No. 906 + No. 89 (3 ramp, 1 playfield) |
| 3 | Q44 | GRY-ORN CN-11 | Left VUK | 23-800 | (2) No. 89 + (2) No. 906 (2 insert, 2 playfield) |
| 4 | Q43 | GRY-YEL CN-11 | Ball Launch | 22-600 | (2) No. 906 + (2) No. 89 (2 insert, 2 playfield) |
| 5 | Q42 | GRY-GRN CN-11 | NO COIL AT THIS LOCATION (NOT USED) | - | (4) No. 89 (4 playfield) |
| 6 | Q41 | GRY-BLU CN-11 | Right VUK | 23-800 | (4) No. 89 (3 playfield, 1 insert) |
| 7 | Q40 | GRY-VIO CN-11 | NO COIL AT THIS LOCATION (NOT USED) | - | (4) No. 89 (4 playfield) |
| 8 | Q39 | GRY-BLK CN-11 | Knocker | 23-800 | (2) No. 89 + (2) No. 906 (2 insert, 2 playfield) |

## Drives 9-16, direct on CN-12

| Drive | Transistor | Wire | Device | Bulbs |
| --- | --- | --- | --- | --- |
| 9 | Q30 | BRN-BLK CN-12 | Flash lamps | (4) No. 89 |
| 10 | Q29 | BLK-RED CN-12 | Left/Right Coil Relay | - |
| 11 | Q28 | BRN-ORN CN-12 | General Illumination Relay | - |
| 12 | Q27 | BRN-YEL CN-12 | Flash lamps | (4) No. 89 |
| 13 | Q26 | BRN-GRN CN-12 | Flash lamps | (4) No. 89 |
| 14 | Q25 | BRN-BLU CN-12 | Flash lamps | (4) No. 89 |
| 15 | Q24 | BRN-VIO CN-12 | Optional Ticket Dispenser | - |
| 16 | Q23 | BRN-GRY CN-12 | Bat Bar Motor | - |

## Drives 17-22, the CPU Controlled Auxiliary Solenoids

| Drive | Description | Control | Power | Transistor | Coil type |
| --- | --- | --- | --- | --- | --- |
| 17 | Left Turbo Bumper | BLU-ORN CPU CN19-3 | RED PS CN3-6 | Q8 | 23-800 |
| 18 | Center Turbo Bumper | BLU-RED CPU CN19-4 | RED PS CN3-6 | Q9 | 23-800 |
| 19 | Right Turbo Bumper | BLU-YEL CPU CN19-6 | RED PS CN3-6 | Q10 | 23-800 |
| 20 | Left Slingshot | BLU-BRN CPU CN19-7 | RED PS CN3-6 | Q11 | 23-800 |
| 21 | Right Slingshot | BLU-GRN CPU CN19-8 | RED PS CN3-6 | Q12 | 23-800 |
| 22 | Motor Circuit | - CPU CN19-9 | - PS CN3-6 | Q13 | - |

## Flipper Solenoids (printed as its own unnumbered table)

| Flipper | Control | Flipper PCB | Power | Coil type |
| --- | --- | --- | --- | --- |
| Left | ORN-GRY CPU CN19-2 | BLU-GRY CN1-9 | GRY-YEL CN2-1,2 | 23-900 |
| Right | ORN-VIO CPU CN19-1 | BLU-VIO CN1-1 | BLK-WHT CN1-1 | 23-900 |

There is no upper flipper of either hand on this table.
