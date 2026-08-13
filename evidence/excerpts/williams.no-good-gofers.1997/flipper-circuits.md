# Williams No Good Gofers operations manual - Flipper circuits and cabinet opto boards

Source: `No_Good_Gofers_OPS.pdf`, SHA-256 `736657e3a0d9c41faa5f6941e3d736ebfcbd66d2649af9dd9798d251df9cb58d`.
Region: PDF pages 125 and 127, printed pages 3-11 (`FLIPPER CIRCUIT DIAGRAM`) and 3-13
(`FLIPPER CABINET SWITCH CIRCUITS`). Transcribed by hand from 300 dpi `pdftoppm` renders.

## Printed page 3-11, FLIPPER CIRCUIT DIAGRAM

Power driver board J119 supply rails, left to right in the drawing: `RED-GRAY +50V`,
`RED-VIOLET +50V`, `RED-BLUE +50V`, `RED-GREEN +50V`. Drives leave on J120:

| J120 pin | Wire | Drive | Transistor | Circuit |
| --- | --- | --- | --- | --- |
| 12 | YELLOW-GREEN | POWER | Q90 | LOWER RIGHT FLIPPER COIL |
| 11 | ORANGE-GREEN | HOLD | Q92 | LOWER RIGHT FLIPPER COIL |
| 9 | YELLOW-BLUE | POWER | Q87 | LOWER LEFT FLIPPER COIL |
| 7 | ORANGE-BLUE | HOLD | Q89 | LOWER LEFT FLIPPER COIL |
| 6 | YELLOW-VIOLET | POWER | Q84 | UPPER RIGHT FLIPPER COIL |
| 4 | ORANGE-VIOLET | HOLD | Q86 | UPPER RIGHT FLIPPER COIL |
| 3 | YELLOW-GRAY | POWER | Q81 | \*BALL LAUNCH RAMP |
| 1 | ORANGE-GRAY | HOLD | Q83 | NOT USED |

The drawing's own footnote, printed verbatim:

```
* The UPPER LEFT FLIPPER circuit is used for the BALL LAUNCH RAMP
```

The same page's `CABINET OPTO SWITCHES` block, fed from CPU board J212:

| J212 pin | Wire | Function | Position | Flipper opto board devices |
| --- | --- | --- | --- | --- |
| 13 | ORANGE | GROUND | - | - |
| 12 | BLUE-VIOLET | L. RIGHT FLIPPER | F2 | U25A-1, U25B-2 |
| 11 | BLUE-GRAY | L. LEFT FLIPPER | F4 | U25C-14, U25D-13 |
| 10 | BLACK-YELLOW | U. RIGHT FLIPPER | F6 | U26A-1, U26B-2 |
| 9 | BLACK-BLUE | U. LEFT FLIPPER | F8 | U26C-14, U26D-13 |

and its `END-OF-STROKE SWITCHES` block, fed from CPU board J208 with `ORANGE GROUND` on pin
14.

## Printed page 3-13, FLIPPER CABINET SWITCH CIRCUITS

The drawing names two physical cabinet opto boards and shows which two positions each carries:

```
CABINET OPTO BOARD (left)        BLUE-GRAY     L. LEFT FLIPPER   F4   J212-11
                                 BLACK-BLUE    U. LEFT FLIPPER   F8   J212-9

RIGHT CABINET OPTO BOARD J1      BLUE-VIOLET   L. RIGHT FLIPPER  F2   J212-12
                                 BLACK-YELLOW  U. RIGHT FLIPPER  F6   J212-10
```

with `GRAY-YELLOW +12V` from power driver J139-2 and `ORANGE GROUND` shared by both boards.

Printed explanatory paragraph, verbatim:

```
The flipper switch circuits operate similar to the dedicated switch circuit. The circuits are
active low and tied to ground through the switch circuit.

When a switch closes, the row side (dedicated input) of the circuit activates. The "+" input
to the LM339 drops below +5V, therefore, its output is low. Since the row, (dedicated input)
circuit is tied directly to ground through the switch, the switch is considered closed by the
microprocessor. When the switch opens, the "+" input to the LM339 is above +5V, its output is
high and the row, (dedicated input) is inactive.
```

Page footers: `3-11` and `3-13`.

## What these pages fix

Each cabinet flipper button carries a two-channel `A-17316` flipper opto board, so one button
feeds both the lower and the upper Fliptronic position on its own side. On this machine the
right-hand board's second channel (F6, public switch 116) is fitted and drives the upper right
flipper, while the left-hand board's second channel (F8, public switch 118) is printed
`NOT USED` on the switch-locations parts list because there is no upper left flipper. The two
pages above print all four positions descriptively because the circuit drawing is the generic
WPC-95 Fliptronic template; fitment comes from the parts list on 2-48, not from these
drawings.

The upper *left* flipper power circuit - Fliptronic solenoid position 35 in PinMAME's public
numbering, printed item 35 in this manual's Flipper Circuits block - drives the Ball Launch
Ramp coil instead of a flipper, and its hold half (36) is unused.
