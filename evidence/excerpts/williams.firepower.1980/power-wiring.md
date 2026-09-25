# Williams Firepower (game 497) — Power Wiring Diagram

Source: `Williams_1980_Firepower_Schematics_paginated_from_manual_dated_March_1980.pdf` (IPDB 856),
PDF page 23, printed page 23, sheet marked `497`. The sheet is printed sideways. Transcribed by hand
from a 130 dpi render checked against a 300 dpi render.

Heading, verbatim: `POWER WIRING`; caption `Power Wiring Diagram`.

## Supplies leaving the power supply board

| Connector | Printed label |
| --- | --- |
| 3P1 | `DISPLAY 90 V.A.C.`, `LAMPS +18 V`, `SOLENOIDS +28 V`, `FLIPPER B+`, `LOGIC SUPPLY 18.7 V.A.C. C.T.` |
| 3P2 | `LAMP GROUND`, `SOLENOID GROUND` (other pins `N.C.`) |
| 10P1 | `SOUND BOARD SUPPLY 18.7 V.A.C. C.T.` |
| 7P1 pins 1-2, 8P2 pins 1-2, 9P1 pins 1, 2, 4, 5 | `6.3 V.A.C. GENERAL ILLUMINATION` |

The lamp supply comes through `LAMP RECTIFIER` `6BR1` with `6C1 30,000 uF` from a `13.5 V.A.C.`
secondary on `BLU`; the solenoid supply through `SOLENOID RECTIFIER` `6BR2` from a `25.5 V.A.C.`
secondary on `RED`.

## General illumination

The `6.3 V.A.C.` secondary (`YEL`, transformer pins 17 and 19) runs through fuse `6F1 20A` on the
fuse card straight to the three `GENERAL ILLUMINATION` outputs: the cabinet (`7P1` pins 1-2, `YEL`
and `YEL-WHT`), the playfield (`8P2` pins 1-2, `YEL` and `WHT-YEL`) and the insert board (`9P1`,
`YEL` and `WHT-YEL`). No relay, transistor or other
switching device is drawn between the transformer and any general-illumination load.

## Notes, verbatim

1. `FOR 105 OR 117 V.A.C., 7.5A FUSE & 130V. VARISTOR #5A-9044 ARE USED.`
2. `FOR 210 OR 235 V.A.C., 4A FUSE & 275 V. VARISTOR #5A-9063 ARE USED.`
3. `JUMPER WIRES ON 6P1 SHOWN WITH SOLIDS LINES ARE CONNECTED FOR 117 V.A.C. OPERATION. ONLY THE ONE
   SHOWN WITH A DASHED LINE IS CONNECTED FOR 220 V.A.C. OPERATION.`
4. `FOR LOW-LINE CONDITIONS (105 OR 210 V.A.C.) MOVE BLK-WHT WIRE FROM 6T1-4 TO 6T1-3 AND MOVE 2
   WHT-RED WIRES FROM 6T1-8 TO 6T1-7.`
5. `FUSES 6F1, 6F2, AND 6F3 ARE MOUNTED ON FUSECARD, LOCATED BELOW POWER SUPPLY BOARD.`

`6F2` and `6F3` (`4A S.B.`) protect the `9.3 V.A.C.` logic windings.
