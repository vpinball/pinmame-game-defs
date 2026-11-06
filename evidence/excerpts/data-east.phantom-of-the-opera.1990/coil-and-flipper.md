# Phantom of the Opera coil and flasher circuits

Source: PDF pages 30-31, printed pages 26-27; PPB connector list PDF page 46, printed page 41; coil wiring PDF page 47, printed page 42; special wiring PDF page 48, printed page 43.

Method: direct visual transcription of the complete printed special/flipper/coil-part tables and every populated branch of the game's coil wiring. project curator; reviewed against native-resolution renders. Drawing labels are factual transcriptions; whole manual pages are retained externally.

## Switch-triggered solenoids

| Coil | Description | Control wire | Control pin | Trigger wire | Trigger pin | Drive transistor (TIP122) | Coil type |
| --- | --- | --- | --- | --- | --- | --- | --- |
| SP1 | Right Pop Bumper | BLU-ORN | CPU CN19-3 | ORN-BLK | CPU CN18-2 | Q8 | 23-800 |
| SP2 | Center Pop Bumper | BLU-RED | CPU CN19-4 | ORN-RED | CPU CN18-3 | Q9 | 23-800 |
| SP3 | Left Slingshot | BLU-YEL | CPU CN19-6 | ORN-YEL | CPU CN18-4 | Q10 | 23-800 |
| SP4 | Left Pop Bumper | BLU-BRN | CPU CN19-7 | ORN-BRN | CPU CN18-5 | Q11 | 23-800 |
| SP5 | Right Slingshot | BLU-GRN | CPU CN19-8 | ORN-GRN | CPU CN18-8 | Q12 | 23-800 |
| SP6 | NOT USED | -- | CPU CN19-9 | -- | CPU CN18-9 | Q13 | -- |

The printed Power Line column is RED / PS CN3-6 for SP1-SP5, and `--` / PS CN3-6 for SP6. The repeated values belong to the separately printed rows. SP6's coil type is `--`; no load is drawn. The special-wiring sheet prints CPU CN16 on the trigger header, where the table and backbox connector list print CN18; the device, wire and pin numbers agree. Follow the own-game table for the structured connector and retain the disagreement as a wiring note.

## Flipper solenoids

| Description | Flipper GND (CPU to coil) | Power lines: switch to flipper PCB | Power lines: PCB to coil | Coil type |
| --- | --- | --- | --- | --- |
| Left Flipper | ORN-GRY CPU CN19-2 | BLU-GRY CN1-9 | GRY-YEL CN2-1,2 | 23-900 |
| Right Flipper | ORN-VIO CPU CN19-1 | BLU-VIO CN1-1 | BLK-WHT CN2-3,4 | 23-900 |

The common Power Input To Flip PCB column prints BLK-WHT / 50VDC and GRY-GRY GRN / 8VAC. The flipper table prints 23-900 for each coil; the part chart lists two 23-900 coils, part 090-5020-30. These are two physical coils; the four public flipper power/hold bits are emulator state.

## Complete coil part-number chart

| Quantity used | Coil type | Data East part number |
| --- | --- | --- |
| 9 | 23-800 | 090-5001-00 |
| 2 | 23-840 | 090-5005-00 |
| 2 | 23-900 | 090-5020-30 |

## Complete populated coil/flash wiring branches

Public numbers 25-29 below correspond to the drawing's SIDE R01-R05; 1-8 are SIDE L01-L08. The public mapping is the K1 mux in pinned s11.c, checked against the retained script. This added public column is not printed by the manual.

| Public | Printed load | CPU transistor | CPU wire | CPU pin | Load-side wire | Load-side pin | Printed coil/bulbs |
| --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | INSERT MASK FLASH | Q46 | GRY-BRN | CPU CN11-1 | VIO-BRN | PPB J9-5 | (3) NO.89 |
| 2 | LEFT CANDELABRA/BACK PANEL LIGHTING/INSERT PHANTOM MASK | Q45 | GRY-RED | CPU CN11-3 | VIO-RED | PPB J9-6 | (1) NO.89 + (3) NO.906 |
| 3 | P.F. PHANTOM MASK | Q44 | GRY-ORN | CPU CN11-4 | VIO-ORN | PPB J9-7 | (4) NO.906 |
| 4 | RIGHT CANDELABRA/SPEAKER HOUSING/BALLERINA INSERT | Q43 | GRY-YEL | CPU CN11-5 | VIO-YEL | PPB J9-8 | (2) NO.89 + (2) NO.906 |
| 5 | LEFT RAMP ENTRANCE/ORGAN INSERT | Q42 | GRY-GRN | CPU CN11-6 | VIO-GRN | PPB J9-9 | (3) NO.89 + (1) NO.906 |
| 6 | P.F. MAGIC MIRROR/YOUNG GIRL INSERT | Q41 | GRY-BLU | CPU CN11-7 | VIO-BLU | PPB J9-10 | (2) NO.89 + (2) NO.906 |
| 7 | SPINNER/JACKPOT/SKULLFACE INSERT | Q40 | GRY-VIO | CPU CN11-8 | VIO-BLK | PPB J9-11 | (2) NO.89 + (2) NO.906 |
| 8 | ORGAN FLASH/PHANTOM INSERT | Q39 | GRY-BLK | CPU CN11-9 | VIO-GRY | PPB J9-12 | (2) NO.89 + (2) NO.906 |
| 9 | TOP RIGHT FLASH | Q30 | BRN-BLK | CPU CN12-1 | BRN-BLK | PPB J9-13 | (4) NO.906 |
| 10 | LEFT/RIGHT COIL RELAY K1 | Q29 | BLK-RED | CPU CN12-2 | BLK-RED | PPB J6-9 | K1 |
| 11 | GENERAL ILLUM. RELAY K1 | Q28 | BRN-ORN | CPU CN12-4 | BRN-ORN | PS CN7-1 | K1 |
| 12 | UNDER LEFT RAMP | Q27 | BRN-YEL | CPU CN12-5 | BRN-YEL | PPB J9-14 | (4) NO.906 |
| 13 | LEFT RAMP MINI MARS | Q26 | BRN-GRN | CPU CN12-6 | BRN-GRN | PPB J9-15 | (4) NO.906 |
| 14 | ORGAN MOTOR | Q25 | BRN-BLU | CPU CN12-7 | WHT-RED | motor relay control board | 25 VAC |
| 15 | RIGHT MINI MARS/MIDDLE LEFT MINI MARS/HANGING MAN INSERT | Q24 | BRN-VIO | CPU CN12-8 | BRN-VIO | PPB J9-2 | (2) NO.89 + (2) NO.906 |
| 16 | LASERKICK | Q23 | WHT-GRY | CPU CN12-9 | BRN-GRY | PPB J8-2 | 23-800 |
| 25 | OUTHOLE | Q46 | GRY-BRN | CPU CN11-1 | BLK-BRN | PPB J2-9 | 23-840 |
| 26 | TROUGH | Q45 | GRY-RED | CPU CN11-3 | BLK-RED | PPB J2-8 | 23-840 |
| 27 | LEFT SIDE MIDDLE VERTICAL UP KICKER | Q44 | GRY-ORN | CPU CN11-4 | BLK-ORN | PPB J2-7 | 23-800 |
| 28 | TOP LEFT SUPER VERTICAL UP KICKER | Q43 | GRY-YEL | CPU CN11-5 | BLK-YEL | PPB J8-4 | 23-800 |
| 29 | RIGHT SIDE MIDDLE SUPER VERTICAL UP KICKER | Q42 | GRY-GRN | CPU CN11-6 | BLK-GRN | PPB J8-7 | 23-800 |

The L01-L08 flasher supply is BRN, +32VL, PPB J6-3; R01-R03 use ORN +32VR PPB J6-4/5. R04/R05 use YEL-VIO +50VR via PPB J7-6/7 and Q4/Q3 on the PPB. The direct flashers 9, 12, 13, 15 use RED +32V; the Laserkick coil uses VIO-YEL +50VDC from PPB J7-3. The motor relay is driven from BRN-BLU/Q25 and switches WHT-RED 25VAC from BR2 in the backbox; its schematic draws a diode across the relay coil and COM/NO/NC contacts.

The game's own PPB J2 connector list names only OUTHOLE, TROUGH, LEFT SIDE MIDDLE VUK, TOP LEFT SUPER VUK and RIGHT SIDE MIDDLE SUPER VUK. It marks the R06/R07/R08 destinations N.U.; no load branch for them is drawn on printed pages 27 or 42. The coil-location drawing nevertheless includes an R08 label near the apron. That isolated label does not identify a knocker or settle the state PinMAME can publish at 32.

## Complete backbox flasher inset

The inset has 16 drawn sockets: L01 points to 3, L02 to 1, L04 to 1, L05 to 3, L06 to 2, L07 to 2, L08 to 2, and 15 to 2. There is no L03 backbox callout. The remaining lamps in each printed total are playfield bulbs. This inset is an elevation, not a registered playfield coordinate drawing.
