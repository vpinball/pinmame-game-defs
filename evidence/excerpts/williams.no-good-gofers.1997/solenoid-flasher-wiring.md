# Williams No Good Gofers operations manual - Solenoid/Flasher Table

Source: `No_Good_Gofers_OPS.pdf`, SHA-256 `736657e3a0d9c41faa5f6941e3d736ebfcbd66d2649af9dd9798d251df9cb58d`.
Region: PDF page 113, printed page 2-53, the `SOLENOID/FLASHER TABLE`. The identical table is
printed again in Section 3 on printed page 3-5 (PDF page 119). Transcribed by hand from a
300 dpi `pdftoppm` render of PDF page 113. Every printed row of every block is reproduced.

The printed column groups are:

```
Sol. No. | Function | Solenoid Type | Voltage Connections (Playfield | Backbox | Cabinet)
         | Drive Xistor | Drive Connections (Playfield | Backbox | Cabinet) | Drive Wire Color
         | Solenoid Part Number / Flashlamp Type (Playfield | Insert)
```

Below, `Voltage` and `Drive` columns are annotated `[PF]`, `[BB]` or `[CAB]` to record which
of the three sub-columns the printed value sits in. Empty cells are shown as `-`.

## Main block

| Sol | Function | Type | Voltage | Xistor | Drive | Wire | Part / Flashlamp (Playfield) | (Insert) |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 01 | AUTO FIRE | High Power | J133-2 [PF] | Q72 | J116-1 [PF] | VIO-BRN | AE-23-800 | - |
| 02 | KICKBACK | High Power | J134-3 [BB] | Q68 | J116-2 [PF] | VIO-RED | AE-23-800 | - |
| 03 | CLUBHOUSE KICKER | High Power | J133-2 [PF] | Q71 | J116-4 [PF] | VIO-ORG | AE-23-800 | - |
| 04 | LEFT GOFER UP | High Power | J133-2 [PF] | Q67 | J116-5 [PF] | VIO-YEL | LE-23-1300 | - |
| 05 | RIGHT GOFER UP | High Power | J133-2 [PF] | Q70 | J116-6 [PF] | VIO-GRN | LE-23-1300 | - |
| 06 | JET POPPER | High Power | J133-2 [PF] | Q66 | J116-7 [PF] | VIO-BLU | AE-27-1200 | - |
| 07 | LEFT EJECT | High Power | J133-2 [PF] | Q69 | J116-8 [PF] | VIO-BLK | AE-24-900 | - |
| 08 | UPPER RIGHT EJECT | High Power | J133-2 [PF] | Q65 | J116-9 [PF] | VIO-GRY | AE-26-1200 | - |
| 09 | TROUGH EJECT | Low Power | J133-3 [PF] | Q44 | J113-1 [PF] | BRN-BLK | AE-26-1500 | - |
| 10 | LEFT SLINGSHOT | Low Power | J133-3 [PF] | Q48 | J113-3 [PF] | BRN-RED | AE-26-1200 | - |
| 11 | RIGHT SLINGSHOT | Low Power | J133-3 [PF] | Q43 | J113-4 [PF] | BRN-ORG | AE-26-1200 | - |
| 12 | TOP JET BUMPER | Low Power | J133-3 [PF] | Q47 | J113-5 [PF] | BRN-YEL | AE-26-1200 | - |
| 13 | MIDDLE JET BUMPER | Low Power | J133-3 [PF] | Q42 | J113-6 [PF] | BRN-GRN | AE-26-1200 | - |
| 14 | BOTTOM JET BUMPER | Low Power | J133-3 [PF] | Q46 | J113-7 [PF] | BRN-BLU | AE-26-1200 | - |
| 15 | LEFT GOFER DOWN | Low Power | J133-3 [PF] | Q41 | J113-8 [PF] | BRN-VIO | AE-30-2000 | - |
| 16 | RIGHT GOFER DOWN | Low Power | J133-3 [PF] | Q45 | J113-9 [PF] | BRN-GRY | AE-30-2000 | - |
| 17 | JET FLASHER | Flasher | J133-6 [PF] | Q28 | J111-1 [PF] | BLK-BRN | #906 | - |
| 18 | LOWER LEFT FLASHER | Flasher | J133-6 [PF] | Q32 | J111-2 [PF] | BLK-RED | #906 | - |
| 19 | LEFT SPINNER FLASHER | Flasher | J133-6 [PF] | Q27 | J111-3 [PF] | BLK-ORG | #906 | - |
| 20 | RIGHT SPINNER FLASHER | Flasher | J133-6 [PF] | Q31 | J111-4 [PF] | BLK-YEL | #906, #89 | - |
| 21 | LOWER RIGHT FLASHER | Flasher | J133-6 [PF] | Q26 | J111-5 [PF] | BLU-GRN | #89 | - |
| 22 | NOT USED | Flasher | J133-6 [PF] | Q30 | - | BLU-BLK | - | - |
| 23 | NOT USED | Flasher | J133-6 [PF] | Q25 | - | BLU-VIO | - | - |
| 24 | UNDERGROUND PASS | Flasher | J133-1 [PF] | Q29 | J111-8 [PF] | BLU-GRY | AE-27-1200 | - |
| 25 | SAND TRAP FLASHER | Gen. Purpose | J133-6 [PF] | Q16 | J109-1 [PF] | BLU-BRN | #906 (2) | - |
| 26 | WHEEL FLASHER | Gen. Purpose | J133-6 [PF] | Q15 | J109-2 [PF] | BLU-RED | #906 | - |
| 27 | LEFT RAMP DOWN | Gen. Purpose | J133-1 [PF] | Q14 | J109-3 [PF] | BLU-ORG | SM1-28-900 | - |
| 28 | RIGHT RAMP DOWN | Gen. Purpose | J133-1 [PF] | Q13 | J109-4 [PF] | BLU-YEL | SM1-28-900 | - |

Items 22 and 23 are the only two rows in this block with a populated drive transistor and a
completely blank Drive Connections group (all three sub-columns empty) and a blank flashlamp
type. Every other row carries a drive connection.

## General Illumination block

| Item | Function | Type | Voltage | Xistor | Drive | Wire | Flashlamp (Playfield) | (Insert) |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 01 | LEFT SIDE STRING | G.I. | J105-1 [PF] | Q5 | J105-7 [PF] | WHT-BRN | - | #555, #545 |
| 02 | RIGHT SIDE STRING | G.I. | J105-2 [PF] | Q4 | J105-8 [PF] | WHT-ORG | - | #555, #545 |
| 03 | GOFER SPOTLIGHT | G.I. | J105-3 [PF] | Q3 | J105-9 [PF] | WHT-YEL | #44 | #555, #545 |
| 04 | *ILLUMINATION STRING 4 | G.I. | J106-5 [BB] | Q2 | J106-10 [BB] | WHT-GRN | #44 | - |
| 05 | *ILLUMINATION STRING 5 | G.I. | J106-6 [BB], J104-3 [CAB] | Q1 | J106-11 [BB], J104-1 [CAB] | WHT-VIO | #44 | - |

## Flipper Circuits block

Printed column groups for this block: `Solenoid Type | Voltage Connection Playfield | Drive
Xistors (Power | Hold) | Drive Connections Playfield | Drive Wire Colors (Power | Hold) | Coil
Part No. | Coil Colors`.

| Sol | Function | Type | Voltage | Power Xistor | Hold Xistor | Drive | Power wire | Hold wire | Coil P/N | Coil colour |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 29 | LOWER RIGHT FLIPPER | Power | J119-1 (RED-GRN) | Q90 | - | J120-13 | YEL-GRN | - | FL-11629 | BLUE |
| 30 | LOWER RIGHT FLIPPER | Hold | J119-1 (RED-GRN) | - | Q92 | J120-11 | - | ORG-GRN | FL-11629 | BLUE |
| 31 | LOWER LEFT FLIPPER | Power | J119-4 (RED-BLU) | Q87 | - | J120-9 | YEL-BLU | - | FL-11629 | BLUE |
| 32 | LOWER LEFT FLIPPER | Hold | J119-4 (RED-BLU) | - | Q89 | J120-7 | - | ORG-BLU | FL-11629 | BLUE |
| 33 | UPPER RIGHT FLIPPER | Power | J119-6 (RED-VIO) | Q84 | - | J120-6 | YEL-VIO | - | FL-11630 | RED |
| 34 | UPPER RIGHT FLIPPER | Hold | J119-6 (RED-VIO) | - | Q86 | J120-4 | - | ORG-VIO | FL-11630 | RED |
| 35 | BALL LAUNCH RAMP | Power | J119-8 (RED-GRY) | Q81 | - | J120-3 | YEL-GRY | - | LE-23-1300-T | YELLOW |
| 36 | NOT USED | Hold | J119-8 (RED-GRY) | - | Q83 | J120-1 | - | ORG-GRY | - | - |

The printed table places the `LOWER RIGHT FLIPPER`, `LOWER LEFT FLIPPER` and `UPPER RIGHT
FLIPPER` function labels once per power/hold pair, straddling the two rows; `BALL LAUNCH RAMP`
sits on the 35 row alone and `NOT USED` on the 36 row alone.

## Motor Circuit block

| Sol | Function | Type | Voltage | Drive Gates | Drive | Wire | Device P/N (Playfield) |
| --- | --- | --- | --- | --- | --- | --- | --- |
| 37 | WHEEL SPIN (counter clock-wise) | Low Power | J139-2 | U3A, U3B | J110-1 | BRN-WHT | SEE BELOW |
| 38 | WHEEL SPIN (clock-wise) | Low Power | J139-2 | U3C, U3D | J110-3 | ORG-WHT | SEE BELOW |

## Auxiliary Circuits block

| Sol | Function | Type | Voltage | Drive Transistor | Drive | Wire | Device P/N (Playfield) |
| --- | --- | --- | --- | --- | --- | --- | --- |
| 42 | UPPER RIGHT 1 FLASHER | Flasher | J4-1 | Q2 | J4-2 | BLU-BRN | #906 |
| 43 | UPPER RIGHT 2 FLASHER | Flasher | J4-1 | Q4 | J4-3 | BLU-RED | #906 |
| 44 | UPPER RIGHT 3 FLASHER | Flasher | J4-1 | Q6 | J4-4 | BLU-ORG | #906 |
| 45 | UPPER PLAYFIELD RIGHT | Flasher | J4-1 | Q8 | J4-5 | BLU-YEL | #906 (2) |
| 46 | UPPER PLAYFIELD LEFT | Flasher | J4-1 | Q10 | J4-7 | BLU-GRN | #906 (2) |
| 47 | UPPER LEFT 3 FLASHER | Flasher | J4-1 | Q12 | J4-8 | BLU-BLK | #906 |
| 48 | UPPER LEFT 2 FLASHER | Flasher | J4-1 | Q14 | J4-9 | BLU-VIO | #906 |
| 49 | UPPER LEFT 1 FLASHER | Flasher | J4-1 | Q16 | J4-10 | BLU-GRY | #906 |

## Printed notes below the blocks, verbatim

```
*These general illumination strings do not brighten and dim, they are always on.
J1XX = Power Driver Board
J4-X = Auxiliary 8-Driver Board

    24-6549 =    #44 bulb
    24-8704 =    #89 bulb
    24-8768 =    #555 bulb
    24-8802 =    #906 bulb

Tieback Diodes:            For solenoids #37 and #38:
    J109-8 & J109-9            Motor, 14-7955-1
    J111-10 & J111-11          DC Motor Control Board, A-16120
                               Motor 2-Opto Board, A-22026
```

The footnote asterisk is carried only by the two rows printed `*ILLUMINATION STRING 4` and
`*ILLUMINATION STRING 5`; general-illumination items 01, 02 and 03 carry no asterisk and
therefore do brighten and dim.

Page footer: `2-53`.
