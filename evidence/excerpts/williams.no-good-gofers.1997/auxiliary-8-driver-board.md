# Williams No Good Gofers operations manual - Auxiliary 8-driver Board A-21773

Source: `No_Good_Gofers_OPS.pdf`, SHA-256 `736657e3a0d9c41faa5f6941e3d736ebfcbd66d2649af9dd9798d251df9cb58d`.
Region: PDF page 138, printed page 3-24, `Auxiliary 8-driver Board A-21773` - the board
layout drawing, its full connector list, and the `Step Flasher Wiring Diagram` below it.
Transcribed by hand from a 300 dpi `pdftoppm` render. Every printed pin is reproduced.

## Connector list, printed verbatim

```
J1      Ribbon Cable, Data to/from CPU J211

J2-1    BLK       Ground from Power Driver Board J139-3
J2-2    GRY-YEL   +12V from Power Driver Board J139-2
J2-3    KEY
J2-4    RED-WHT   +20V from Power Driver Board J134-5
J2-5    BLK       Ground from Power Driver Board J137-4

J3      NOT USED

J4-1    RED-WHT   +20V to Step Flashers
J4-2    BLU-BRN   Solenoid #42 drive to Upper Right 1 Flasher
J4-3    BLU-RED   Solenoid #43 drive to Upper Right 2 Flasher
J4-4    BLU-ORG   Solenoid #44 drive to Upper Right 3 Flasher
J4-5    BLU-YEL   Solenoid #45 drive to Upper Right Playfield Flasher
J4-6    KEY
J4-7    BLU-GRN   Solenoid #46 drive to Upper Left Playfield Flasher
J4-8    BLU-BLK   Solenoid #47 drive to Upper Left 3 Flasher
J4-9    BLU-VIO   Solenoid #48 drive to Upper Left 2 Flasher
J4-10   BLU-GRY   Solenoid #49 drive to Upper Left 1 Flasher
```

## Step Flasher Wiring Diagram

The diagram redraws the same eight drives, showing the CPU board's J211 ribbon cable feeding
the auxiliary board's J1, the power-driver board's J139-1/2 (ground, +12V) and J137-4/5
(ground, +20V) feeding J2, and J4 fanning out to the flashlamps. Each J4 pin's label in the
diagram:

| J4 pin | Wire | Label |
| --- | --- | --- |
| 1 | RED-WHT | (supply) |
| 2 | BLU-BRN | SOLENOID 42 UPPER RIGHT 1 FLASHER |
| 3 | BLU-RED | SOLENOID 43 UPPER RIGHT 2 FLASHER |
| 4 | BLU-ORG | SOLENOID 44 UPPER RIGHT 3 FLASHER |
| 5 | BLU-YEL | SOLENOID 45 UPPER PLAYFIELD RIGHT FLSHRS |
| 7 | BLU-GRN | SOLENOID 46 UPPER PLAYFIELD LEFT FLSHRS |
| 8 | BLU-BLK | SOLENOID 47 UPPER LEFT 3 FLASHER |
| 9 | BLU-VIO | SOLENOID 48 UPPER LEFT 2 FLASHER |
| 10 | BLU-GRY | SOLENOID 49 UPPER LEFT 1 FLASHER |

Pins 5 and 7 are each drawn with **two** lamp symbols in series with the supply rail; the six
other drives are drawn with one lamp symbol each. That matches the `(#906, 2 BULBS)` marker
the parts list on 2-44 carries for items 45 and 46 only.

The connector-list note on J4-5 reads `Upper Right Playfield Flasher` while both the parts
list on 2-44 and this diagram read `UPPER PLAYFIELD RIGHT`; the words are transposed on the
connector list only.

Page footer: `3-24`.
