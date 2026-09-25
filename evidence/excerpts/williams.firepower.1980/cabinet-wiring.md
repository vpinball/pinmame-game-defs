# Williams Firepower (game 497) — Cabinet Wiring Diagram

Source: `Williams_1980_Firepower_Schematics_paginated_from_manual_dated_March_1980.pdf` (IPDB 856),
PDF page 24, printed page 24, sheet marked `497`. The sheet is printed sideways. Transcribed by hand
from a 300 dpi render.

Heading, verbatim: `CABINET WIRING DIAGRAM`; caption `Cabinet Wiring Diagram`.

## Notes, verbatim

1. `FLIPPER SWITCH CONTACTS AND WIRING SHOWN WITH DASHED LINES ARE USED ONLY IN GAMES WITH DUAL
   ACTION FLIPPERS.`
2. `JUMPER WIRES ON 6P1 SHOWN WITH SOLID LINES ARE CONNECTED FOR 117VAC OPERATION. FOR 220VAC
   OPERATION THE ONE SHOWN WITH A DASHED LINE IS CONNECTED. ALL JUMPERS ARE WHT-RED.`

## Matrix column 1 switches

Each switch is drawn as a normally open contact with a series diode. Switches 1-3 connect on
`7J1`; switches 4-8 connect on `7J2`/`7P2`, the coin-door connector, and share the common on
`7J2-6`.

| Switch | Printed name | Diode | Connection |
| --- | --- | --- | --- |
| 7SW1 | PLUMB BOB TILT | 7D1 | 7J1 |
| 7SW2 | BALL ROLL TILT | 7D2 | 7J1 |
| 7SW3 | CREDIT BUTTON | 7D3 | 7J1 |
| 7SW4 | RIGHT COIN CHUTE | 7D4 | 7J2-8 |
| 7SW5 | CENTER COIN CHUTE | 7D5 | 7J2-9 |
| 7SW6 | LEFT COIN CHUTE | 7D6 | 7J2-10 |
| 7SW7 | SLAM TILT | 7D7 | 7J2-11 |
| 7SW8 | HIGH SCORE RESET | 7D8 | 7J2-12 |

The column-1 strobe reaches the cabinet as `COL. 1` from `2J2-9` on `2P2-9` wire `GRN-BRN`, and the
eight row returns come from `2J3`/`2P3` pins 9, 8, 7, 6, 5, 4, 3, 1 (`ROW 1` to `ROW 8`) on wires
`WHT-BRN`, `WHT-RED`, `WHT-ORN`, `WHT-YEL`, `WHT-GRN`, `WHT-BLU`, `WHT-VIO`, `WHT-GRY` to `7P1`
pins 21 to 28.

## Service switches

| Switch | Printed name | Connection |
| --- | --- | --- |
| 7SW74 | a changeover switch with positions `AUTO-UP` and `MANUAL-DOWN` | 7J2-15, 7J1-6, `BLU`, `1P4-4` `AUTO./MAN.` |
| 7SW75 | ADVANCE | 7J2-14, 7J1-5, `GRN`, `1P4-3` `ADVANCE` |
| 7SW76 | MEMORY PROTECT INTERLOCK | 7J1-34, `BLK-RED`, `1P4-1` `MEM. PROT.` |

`1P4-2` is `GRD.` on `WHT` (7J1-4). `1J4` is labelled `CPU BOARD`.

## Coils

| Coil | Printed name | Diode | Drive |
| --- | --- | --- | --- |
| 7L14 | CREDIT KNOCKER | 7D9 | 7J1-16, `BRN-BLU`, `2J9-4` `SOL.14 (Q41)` |
| 7L16 | COIN LOCKOUT | 7D10 | 7J2-4 |

Their supply is `+28V` on `RED` from `3J3-7` (7J1-3). `2J9-6` `SOL.16 (Q45)` leaves on `BRN-GRY`.

## Flipper buttons

`7SW72 RIGHT FLIPPER (NOTE 1)` and `7SW73 LEFT FLIPPER (NOTE 1)`, each drawn as one solid contact
with a second, dashed contact beside it. The flipper-button returns come from `2J12`/`2P12`,
labelled `FLIPPER GRD`: pin 1 `ORN-VIO` to `7P1-7` (right button) and pin 2 `ORN-GRY` to `7P1-9`
(left button). The coil sides go to `8J3`/`8P3`, labelled `PLAYFIELD FLIPPER COILS`: `BLU-VIO`
`7P1-8` to `8P3-3`, `BLU-GRY` `7P1-10` to `8P3-4`, and the dashed dual-action wires `BLK-YEL (NOTE
1)` `7P1-31` to `8P3-15` and `BLK-BLU (NOTE 1)` `7P1-30` to `8P3-9`.

## Other cabinet items

- `SPEAKER` from `10P2`/`10J2` (`AUDIO`, `GRD`) on `BLK-BRN` and `BLACK`, and `7R1 REMOTE VOLUME` on
  `10P4`/`10J4` (`AUDIO OUT`, `AUDIO IN`, `SHIELD`).
- `GENERAL ILLUMINATION`: three bulbs across `7J2`/`7P2` pins 1 and 2, fed from `7J1` pins 1 and 2 on
  `YEL` and `YEL-WHT` from the `FUSE CARD` (`6.3VAC`). No switching device is drawn in this circuit.
- `7SW71 ON/OFF SWITCH`, `7LF1 LINE FILTER`, `7VR1`, `7F1 A.C. FUSE`, `UTILITY OUTLET`, `A.C. LINE
  CORD`, and the transformer primary jumpers on `6J1`/`6P1`.
