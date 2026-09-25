# Sega GoldenEye (1996) — Switch Matrix Grid and Dedicated Switches

Source: Sega Pinball *GoldenEye* operations manual (132-page image-only scan,
`Sega_1996_Goldeneye_Manual.pdf`), PDF page 32, printed page 20 (Section 3, Chapter 2), table
**SWITCH MATRIX GRID** and **Dedicated Switches**. Read from the native 300 dpi render. The same
grid is reprinted on the Find-It-In-Front page iii (PDF page 5) with the same cells.

Printed legend above the grid: typical switch schematic with column (switch drive) wire `GRN-XXX` to
the N.O. terminal, row (switch return) wire `WHT-XXX` through a blocking diode to the common
terminal; dedicated switch schematic `GRY-XXX` to N.O., `BLK` ground to common.

## Column header (drive)

| Column | Transistor | Wire | Connector |
| --- | --- | --- | --- |
| 1 | Q1 | GRN-BRN | CN5-1 |
| 2 | Q2 | GRN-RED | CN5-3 |
| 3 | Q3 | GRN-ORG | CN5-4 |
| 4 | Q4 | GRN-YEL | CN5-5 |
| 5 | Q5 | GRN-BLK | CN5-6 |
| 6 | Q6 | GRN-BLU | CN5-7 |
| 7 | Q7 | GRN-VIO | CN5-8 |
| 8 | Q8 | GRN-GRY | CN5-9 |

## Row header (return)

| Row | Wire | Connector |
| --- | --- | --- |
| 1 | WHT-BRN | CN7-9 |
| 2 | WHT-RED | CN7-8 |
| 3 | WHT-ORG | CN7-7 |
| 4 | WHT-YEL | CN7-6 |
| 5 | WHT-GRN | CN7-5 |
| 6 | WHT-BLU | CN7-3 |
| 7 | WHT-VIO | CN7-2 |
| 8 | WHT-GRY | CN7-1 |

## Cells (printed switch number in the black box)

| No. | Printed text | No. | Printed text |
| --- | --- | --- | --- |
| 1 | PLUMB BOB TILT | 33 | 2-BANK BOTTOM |
| 2 | 4TH COIN SLOT | 34 | 2-BANK TOP |
| 3 | START BUTTON | 35 | NOT USED (shaded) |
| 4 | RIGHT COIN SLOT | 36 | NOT USED (shaded) |
| 5 | CENTER COIN SLOT / DBA | 37 | NOT USED (shaded) |
| 6 | LEFT COIN SLOT | 38 | NOT USED (shaded) |
| 7 | SLAM TILT | 39 | EJECT STAND-UP |
| 8 | NOT USED (shaded) | 40 | LEFT RAMP ENTER |
| 9 | FIRE BUTTON | 41 | LEFT TURBO BUMPER |
| 10 | 5-BALL TROUGH #1 (LEFT) | 42 | BOTTOM TURBO BUMPER |
| 11 | 5-BALL TROUGH #2 | 43 | RIGHT TURBO BUMPER |
| 12 | 5-BALL TROUGH #3 | 44 | RIGHT 5-BANK TOP |
| 13 | 5-BALL TROUGH #4 | 45 | RIGHT 5-BANK MID-TOP |
| 14 | 5-BALL TROUGH #5 (RIGHT) | 46 | RIGHT 5-BANK MIDDLE |
| 15 | 5-BALL TROUGH VUK OPTO | 47 | RIGHT 5-BANK MID-BOT |
| 16 | SHOOTER LANE | 48 | RIGHT 5-BANK BOTTOM |
| 17 | RIGHT RAMP EXIT | 49 | NOT USED (shaded) |
| 18 | CENTER RAMP EXIT | 50 | SCOOP |
| 19 | RIGHT RAMP ENTER | 51 | RIGHT TOP LANE |
| 20 | SATELLITE HOME | 52 | MIDDLE TOP LANE |
| 21 | NOT USED (shaded) | 53 | LEFT TOP LANE |
| 22 | NOT USED (shaded) | 54 | CENTER RAMP ENTER |
| 23 | SATELLITE MAGNET BOARD | 55 | TOP LANE ENTER |
| 24 | FLIPPER MAGNET BOARD | 56 | TANK TRAP DOOR |
| 25 | LEFT 5-BANK BOTTOM | 57 | LEFT OUTLANE |
| 26 | LEFT 5-BANK MID-BOT | 58 | RIGHT OUTLANE |
| 27 | LEFT 5-BANK MIDDLE | 59 | LEFT RETURN LANE |
| 28 | LEFT 5-BANK MID-TOP | 60 | RIGHT RETURN LANE |
| 29 | NOT USED (shaded) | 61 | LEFT SLINGSHOT |
| 30 | LEFT STAND-UP | 62 | RIGHT SLINGSHOT |
| 31 | RIGHT STAND-UP | 63 | LT FLIPPER BUTTON VIA Q7 (ON SSFB) |
| 32 | LEFT RAMP MADE | 64 | RT FLIPPER BUTTON VIA Q5 (ON SSFB) |

The number box of cell 29 is overprinted by the shading and reads like `25`; its position (column 4,
row 5) is switch 29.

## Dedicated switches (IC U206 inputs, ground BLK CN6-1)

| DS | Wire | Connector | Printed text |
| --- | --- | --- | --- |
| DS-1 | GRY-BRN | CN6-2 | NOT USED (shaded) |
| DS-2 | GRY-RED | CN6-3 | NOT USED (shaded) |
| DS-3 | GRY-ORG | CN6-4 | NOT USED (shaded) |
| DS-4 | GRY-YEL | CN6-6 | NOT USED (shaded) |
| DS-5 | GRY-GRN | CN6-7 | NOT USED (shaded) |
| DS-6 | GRY-BLU | CN6-8 | Normal: Volume. In Test: Left. RED BUTTON |
| DS-7 | GRY-VIO | CN6-9 | Normal: Service Credits. In Test: Right. GRN BUTTON |
| DS-8 | GRY-BLK | CN6-10 | Normal: Begin Test. In Test: Enter. BLK BUTTON |
