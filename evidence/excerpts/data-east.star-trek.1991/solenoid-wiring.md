# Flash lamp and coil circuits

Read from the Data East operations manual, printed pp. 28–29 (PDF pp. 9–10 of the Arcade Museum scan). The schematic labels below preserve the printed L/R sides of the PPB relay. The B labels on the location drawing and the R labels in the schematic designate the same flasher circuits. `INSERT` in this schematic is the backbox insert panel, which the preceding page draws separately from the playfield. Quantities are per circuit. Bulb-type quantities apply to the entire circuit and do not assign a particular bulb type to an individual socket.

| Side L / A | Coil or load | Coil type | Coil return at load | Supply at load | Side R / B routing label | Flasher bulbs |
| --- | --- | --- | --- | --- | --- | --- |
| 01 | OUTHOLE | 23-840 | VIO-BRN | BRN | 4 PLFD | (2) NO. 89, (2) NO. 906 |
| 02 | TROUGH EJECT | 23-840 | VIO-RED | BRN | 2 INSERT, 2 RAMP | (2) NO. 89, (2) NO. 906 |
| 03 | TURBO BOOST KICKER | 22-800 | VIO-ORG | YEL-VIO | 2 INSERT, 2 PLFD | (2) NO. 906, (2) NO. 89 |
| 04 | LEFT DROP TARGETS | 23-800 | VIO-YEL | BRN | 2 INSERT, 2 PLFD | (2) NO. 906, (2) NO. 89 |
| 05 | RAMP UP | 23-840 | VIO-GRN | BRN | 2 RAMP, 2 INSERT | (2) NO. 89, (2) NO. 906 |
| 06 | RAMP DOWN | 31-1800 | VIO-BLU | YEL-VIO | 2 INSERT, 2 RAMP | (2) NO. 89, (2) NO. 906 |
| 07 | RIGHT DROP TARGET | 23-800 | VIO-BLK | BRN | 1 PLFD, 3 INSERT | (3) NO. 89, (1) NO. 906 |
| 08 | 50V KNOCKER | 23-800 | VIO-GRY | YEL-VIO | 1 PLFD, 3 INSERT | (3) NO. 89, (1) NO. 906 |

The CPU CN-11 ties the L/R pair to one drive. In the same order, CN-11 uses pins 1, 2, 4, 5, 6, 7, 8 and 9, driven by Q46 through Q39, with wires GRY-BRN, GRY-RED, GRY-ORN, GRY-YEL, GRY-GRN, GRY-BLU, GRY-VIO and GRY-BLK. The corresponding PPB J2 flasher branches use pins 9, 8, 7, 6, 5, 4, 2 and 1, on BLK-BRN, BLK-RED, BLK-ORN, BLK-YEL, BLK-GRN, BLK-BLU, BLK-VIO and BLK-GRY. The PPB provides separate +32VL and +32VR, plus +50VL/+50VR where drawn. The turbo boost kicker, ramp-down and knocker coil branches use TIP 36C power drivers.

| Coil no. | CPU CN-12 pin | CPU wire | CPU driver | Load on schematic |
| --- | --- | --- | --- | --- |
| 09 | 1 | BRN-BLK | Q30 | 1 INSERT, 3 PLFD, (4) NO. 89 |
| 10 | 2 | BLK-RED | Q29 | LEFT/RIGHT COIL RELAY |
| 11 | 4 | BRN-ORN | Q28 | GENERAL ILLUM. RELAY K-1, PS board CN7-3 |
| 12 | 5 | BRN-YEL | Q27 | 2 PLFD, 2 BACK PANEL, (4) NO. 89 through PPB R-11 |
| 13 | 6 | BRN-GRN | Q26 | SPECIAL EFFECTS MOTOR relay and 28 VAC motor 515-5532-00-14 |
| 14 | 7 | WHT-BLU | Q25 | TRANSPORTER LAUNCH, PPB J8-6 to Q3 then J8-7 |
| 15 | 8 | WHT-VIO | Q24 | LASER KICK, PPB J8-11 to TIP 36 C Q1 then J8-12 |
| 16 | 9 | BRN-GRY | Q23 | SWINGING TARGET MOTOR relay and 28 VAC motor 515-5534-00 |

## CPU Controlled Auxiliary Solenoids

| Coil Number | Coil Description | Control Line (CPU to Coil) | Power Line (PS to Coil) | Drive Transistor | Coil Type |
| --- | --- | --- | --- | --- | --- |
| 17 | Left Turbo Bumper | BLU-ORN CPU CN19-3 | RED PS CN3-6 | Q8 | 23-800 |
| 18 | Center Turbo Bumper | BLU-RED CPU CN19-4 | RED PS CN3-6 | Q9 | 23-800 |
| 19 | Right Turbo Bumper | BLU-YEL CPU CN19-6 | RED PS CN3-6 | Q10 | 23-800 |
| 20 | Left Slingshot | BLU-BRN CPU CN19-7 | RED PS CN3-6 | Q11 | 23-800 |
| 21 | Right Slingshot | BLU-GRN CPU CN19-8 | RED PS CN3-6 | Q12 | 23-800 |
| 22 | Gate (See Schematic) | BLU-BLK CPU CN19-9 | RED PS CN3-6 | Q13 | 31-1800 |

## Flipper Solenoids

The `Flipper GND` heading spans the CPU-to-coil and switch-to-board columns. The power-input cell is shared by both rows.

| Coil Description | CPU to Coil | Sw. to Flip.PCB | Power Lines FlipPc to Coil | Coil Type | Power Input To Flip PCB |
| --- | --- | --- | --- | --- | --- |
| Left Flipper 090-5030-00 | ORN-GRY CPU CN19-2 | BLU-GRY CN1-9 | GRY-YEL CN2-1,2 | 23-1100 | BLK-WHT 50VDC, GRY, GRY-GRN 8VAC |
| Right Flipper 090-5030-00 | ORN-VIO CPU CN19-1 | BLU-VIO CN1-1 | BLK-WHT CN1-1 | 23-1100 | [shared power-input cell above] |
