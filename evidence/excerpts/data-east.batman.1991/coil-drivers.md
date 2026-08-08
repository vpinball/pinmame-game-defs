# Batman (Data East 1991) - Coil drivers and the Left/Right relay

Transcribed by hand from 400 dpi renders of printed pages 28 and 29 (PDF 32 and 33). This manual has no text layer at all (70 pages, 0 characters), so nothing here came from `pdftotext`.

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

| Drive | Transistor | Wire | Device | Bulbs | Printed placement |
| --- | --- | --- | --- | --- | --- |
| 9 | Q30 | BRN-BLK CN-12 | Flash lamps | (4) No. 89 | 3 insert, 1 playfield |
| 10 | Q29 | BLK-RED CN-12 | Left/Right Coil Relay | - | - |
| 11 | Q28 | BRN-ORN CN-12 | General Illumination Relay | - | - |
| 12 | Q27 | BRN-YEL CN-12 | Flash lamps | (4) No. 89 | 3 insert, 1 playfield |
| 13 | Q26 | BRN-GRN CN-12 | Flash lamps | (4) No. 89 | 2 insert, 2 playfield |
| 14 | Q25 | BRN-BLU CN-12 | Flash lamps | (4) No. 89 | 4 insert |
| 15 | Q24 | BRN-VIO CN-12 | Optional Ticket Dispenser | - | - |
| 16 | Q23 | BRN-GRY CN-12 | Bat Bar Motor | - | 2 insert, 2 playfield |

## Drives 17-22, the CPU Controlled Auxiliary Solenoids

| Drive | Description | Control | Power | Transistor | Coil type |
| --- | --- | --- | --- | --- | --- |
| 17 | Left Turbo Bumper | BLU-ORN CPU CN19-3 | RED PS CN3-6 | Q8 | 23-800 |
| 18 | Center Turbo Bumper | BLU-RED CPU CN19-4 | RED PS CN3-6 | Q9 | 23-800 |
| 19 | Right Turbo Bumper | BLU-YEL CPU CN19-6 | RED PS CN3-6 | Q10 | 23-800 |
| 20 | Left Slingshot | BLU-BRN CPU CN19-7 | RED PS CN3-6 | Q11 | 23-800 |
| 21 | Right Slingshot | BLU-GRN CPU CN19-8 | RED PS CN3-6 | Q12 | 23-800 |
| 22 | Motor Circuit (See Schematic) | - CPU CN19-9 | - PS CN3-6 | Q13 | - |

## Flipper Solenoids (printed as its own unnumbered table)

| Flipper | Control | Flipper PCB | Power lines to coil | Coil type | Power input to flipper PCB |
| --- | --- | --- | --- | --- | --- |
| Left | ORN-GRY CPU CN19-2 | BLU-GRY CN1-9 | GRY-YEL CN2-1,2 | 23-900 | BLK-WHT 50 VDC; GRY and GRY-GRN 8 VAC |
| Right | ORN-VIO CPU CN19-1 | BLU-VIO CN1-1 | BLK-WHT CN1-1 | 23-900 | BLK-WHT 50 VDC; GRY and GRY-GRN 8 VAC |

The table enumerates only Left Flipper and Right Flipper. The conclusion that this machine has no upper flipper is an interpretation corroborated by the game-data flipper mask, not a separate printed row.

## Printed page 28 location drawings

The accompanying crop preserves the complete numbered playfield plan and Backbox Flash Lamps inset. It independently locates auxiliary solenoids 17, 18, and 19 as left, lower-centre, and right in the turbo-bumper cluster; 20 and 21 at the left and right slingshots; and drive 22 beside the right-side ramp-diverter assembly. The `1A`-`8A` and `1B`-`8B` callouts show that a single numbered flash-lamp drive can feed several bulbs and can span playfield, insert, ramp, and backbox positions; they are not one point device per address.

## Bat Bar motor circuit on printed page 29

The drive-16 branch passes through a relay board that switches a 28 VAC feed to `BATBAR MOTOR ASSY. 515-5256-00-11`. This establishes the motor voltage and assembly part number. It does not identify the device behind drive 22, whose printed auxiliary-solenoid row remains only `Motor Circuit (See Schematic)`; the retained known-working script supplies the runtime evidence that public 22 controls the ramp diverter.
