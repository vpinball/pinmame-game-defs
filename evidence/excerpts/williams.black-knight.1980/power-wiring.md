# Williams Black Knight (game 500) - Power Wiring Diagram (power supply board)

Source: `Williams_1980_Black_Knight_English_Manual_with_paginated_schematics.pdf`, PDF page 42. The sheet is upright portrait (5101 x 6802 px at 600 dpi, `render\man600-42.png`), no rotation applied. It carries no printed title, sheet number or page number in the portion I could find (the sheet appears to be the right-hand part of a larger diagram: the left-hand wires from 3P1, 3P2, 3P9, the lamp rectifier bridges and the 6BR2 bridge run off the left edge of the page without labels; a faint vertical dotted fold/panel line runs through the 3P5-3P8 connector columns). Read from zoomed 600 dpi tiles (`crops2\pw-*.png`), 1.0x-2.2x.

Normalization: none. All text transcribed as printed. Wire colours are only printed on the right-hand (harness) side of the connector pairs on the right of the power supply board; the wires on the left of the board carry no colour labels. Each connector appears as a pair of rectangles: the left rectangle is the connector on the outside of the board edge (3Pn, harness-side, left of the printed pin number column) and the right rectangle is the board-side header (the one with arrows `<-` pointing into the board). The Power Supply Board is the large rectangle in the middle, labelled `POWER SUPPLY BOARD` near the bottom. For connectors on the right of the board, the pin-number column sits between the board-side arrows and the harness-side contacts, so pin numbers apply to both sides of each connector.

## Left of the board (connectors 3P1, 3P2, 3P9, 10P1 and rectifier bridges)

### 10P1 (top, above 3P1): label `SOUND BOARD SUPPLY 18.7 V.A.C. C.T.`

Pins drawn: `9`, `5`, `1` (bracketed, labelled `SOUND BOARD` / `SUPPLY 18.7 V.A.C. C.T.`). Each pin has a wire running left, turning down and joining a 3P1 line (junction dots): `10P1-9` -> 3P1 pin 11; `10P1-5` -> 3P1 pin 12; `10P1-1` -> 3P1 pin 10. No wire colours printed.

### 3P1 (harness side, pins 4, 9, 10, 12, 11, 6, 7, 1, 5, 8, 2, 3, in this vertical order)

| 3P1 pin | Left (harness) side | Board side |
|---|---|---|
| 4 | line running off the left edge (no label) | via `F1` `0.25ASB` to the `+100V.D.C. / -100V.D.C. SUPPLIES` block |
| 9 | line running off the left edge | ground symbol |
| 10 | line running off the left edge; junction with the 10P1-1 wire | via `F5` `7ASB` to the `+5V.D.C. / +12V.D.C. / -12V.D.C. SUPPLIES` block |
| 12 | line running off the left edge; junction with the 10P1-5 wire | ground symbol |
| 11 | line running off the left edge; junction with the 10P1-9 wire | via `F6` `7ASB` to the `+5V.D.C. / +12V.D.C. / -12V.D.C. SUPPLIES` block |
| 6 | `N.C.` | `N.C.` |
| 7 | `N.C.` | `N.C.` |
| 1 | `N.C.` | `N.C.` |
| 5 | `N.C.` | `N.C.` |
| 8 | from the `LAMP RECTIFIER` `6BR1` + output (label `V10`) through the connector `P/O 6J1` pin 7 / `P/O 6P1` pin 7 | via `F3` `8ASB`, label `+18V.D.C.` |
| 2 | from the connector pair `P/O 6J1`/`P/O 6P1` pin 1, wire label `ORN`, which joins the `6BR2` + output and the `6C1` capacitor net | via `F2` `2.5ASB` to the `SOLENOID B+` block, output label `+38` |
| 3 | same node as pin 2 (the pin-2 and pin-3 lines are joined by a junction after `6P1`-1) | via `F4` `20A`, no regulator block |

Lamp rectifier network (left, partly off the page): label `LAMP RECTIFIER` over the bridge `6BR1` (diode bridge, `+` terminal on the right with label `+`, both `A.C.` input labels); a second bridge `6BR2` below it (`+` terminal on the right, `A.C.` inputs); the capacitor `6C1` marked `+`, value `30,000uF` (printed `30,000µF`), connected from the `6BR1` + node (label `V10`) down to the common return line, which runs to 3P2. The `6BR2` + output joins the `ORN` line going to `6J1`/`6P1` pin 1. The connector pieces are labelled `P/O 6J1` and `P/O 6P1` (each drawn with a broken-line break symbol between them), pins `7` and `1` printed in between.

### 3P2 (pins 6, 3, 2, 4, 1, 5)

| 3P2 pin | Left side | Board side |
|---|---|---|
| 6 | line from the `6C1` / bridge common return | ground symbol |
| 3 | line running off the left edge | ground symbol |
| 2 | `N.C.` | `N.C.` |
| 4 | `N.C.` | `N.C.` |
| 1 | `N.C.` | `N.C.` |
| 5 | `N.C.` | `N.C.` |

### 3P9 (pins 2, 1)

| 3P9 pin | Left side | Board side |
|---|---|---|
| 2 | line running off the left edge | via fuse labelled `F6` `20A` to a line that runs right, then down (outer vertical, x about 2770 px) to 3P8 pins 6, 7, 8, 9 (board side) |
| 1 | line running off the left edge | through the `K1 SPECIAL RELAY` contact (see below) to a line that runs right, then down (inner vertical, x about 2700 px) to 3P8 pins 1, 2, 3, 4 (board side) |

## Fuses (as printed)

| Designator | Rating | Location |
|---|---|---|
| F1 | 0.25ASB | 3P1 pin 4, feeding the +100/-100 V supply block |
| F5 | 7ASB | 3P1 pin 10, feeding the +5/+12/-12 V supply block |
| F6 | 7ASB | 3P1 pin 11, feeding the +5/+12/-12 V supply block |
| F3 | 8ASB | 3P1 pin 8, +18V.D.C. output line |
| F2 | 2.5ASB | 3P1 pin 2, feeding the SOLENOID B+ block |
| F4 | 20A | 3P1 pin 3, flipper B+ line |
| F6 (second use of the designator) | 20A | 3P9 pin 2 |

Six designators F1-F6 appear but `F6` is printed twice: once as `F6` / `7ASB` (3P1 pin 11) and once as `F6` / `20A` (3P9 pin 2). `F5` is `7ASB` (3P1 pin 10). There is no second fuse labelled F4 or F5.

## Supply blocks inside the board (as printed)

- `+100V.D.C. / -100V.D.C. / SUPPLIES` block, fed through F1. Outputs labelled `+100V.D.C.` (to 3P5 pin 4) and `-100V.D.C.` (to 3P5 pin 3); a ground symbol drawn at its lower left.
- `+5V.D.C. / +12V.D.C. / -12V.D.C. / SUPPLIES` block, fed through F5 and F6, with a ground symbol at its left. Outputs labelled `+5V.D.C.`, `+12V.D.C.`, `-12V.D.C.`. The `+5V.D.C.` line feeds a vertical bus (junction dot) that goes up to 3P5 pin 6 and down to 3P6 pins 4, 10, 9, 8, 7; the `+12V.D.C.` line turns down (vertical bus) to 3P6 pins 3 and 6 (junction dot at pin 3, pin 6 on the same vertical); the `-12V.D.C.` line turns down (separate vertical) to 3P6 pin 2.
- `SOLENOID B+` block, fed through F2, output labelled `+38`: feeds 3P3 pins 8, 7, 6 (junction dots).
- `+18V.D.C.` line from F3 (no block): turns down to 3P4 pins 5, 6, 7, 8 (junction dots).
- The F4 `20A` line goes to 3P3 pins 5 and 4.

## Right of the board (harness connectors)

All wire colour labels are as printed on the right-hand harness side of the pin columns.

### 3P5 -> 4P7 (Master Display)

| 3P5 pin (board-side supply) | Wire colour | 4P7 pin |
|---|---|---|
| 4 (+100V.D.C.) | BRN | 2 |
| 3 (-100V.D.C.) | ORN, WHT-BLK (printed `ORN, WHT-BLK`; the line has a junction dot after which a branch also goes to 4P7 pin 1) | 6 and 1 |
| 6 (+5V.D.C.) | GRY | 3 |
| 1 (ground) | BLK | 5 |

4P7 pins in vertical order as printed: 2, 1, 6, 3, 5; bracket label `MASTER DISPLAY`. Pin 1 is joined by the junction on the ORN, WHT-BLK wire (it has no wire of its own).

### 3P3 (solenoid / special-switch / flipper supplies)

| 3P3 pin | Board side | Wire colour | Goes to |
|---|---|---|---|
| 1 | `NC` (stub line only) | stub, no label | nothing drawn |
| 2 | `NC` (stub line only) | stub, no label | nothing drawn |
| 3 | ground | BLK | 8P3 pin 35, label `SPEC. SW. GND` (bracket `PLAYFIELD`) |
| 6 | +38 (Solenoid B+) | RED | 8P3 pin 36, label `SOL. B+` (bracket `PLAYFIELD`) |
| 7 | +38 (Solenoid B+) | RED | 7P1 pin 3, label `SOL. B+ CABINET` |
| 8 | +38 (Solenoid B+) | RED | a long vertical (x about 3690 px) that runs down the sheet to a horizontal line that continues left to 3P7 pin 3 (see K1 below) |
| 4 | F4 `20A` line | ORN | 8P2 pin 23, label `FLIPPER` (bracket `PLAYFIELD`) |
| 5 | F4 `20A` line | ORN | 8P2 pin 24, label `B+` (bracket `PLAYFIELD`) |

### 3P4 (+18 V and ground to the lamp, solenoid-driver and CPU-side boards)

3P4 harness-side pins and wire colours, in vertical order as printed: 5 `BLU`, 6 `BLU`, 7 `BLU`, 8 `BLU`, 9 `BLK`, 10 `BLK`, 11 `BLK`, 12 `BLK`, 1 `BLK`, 2 `BLK`, 3 `BLK`, 4 `BLK`. Board side: pins 5, 6, 7, 8 are on the `+18V.D.C.` vertical (junction dots on 5, 6, 7); pins 9, 10, 11, 12, 1, 2, 3, 4 are on a common ground bus (junction dots) ending in a ground symbol.

- Pins 5-8 (BLU x4) go into a bold (bundle) line that ends at `2P4` (pins 1, 2, 4, 5, 6, 7, 8, 9 and a `KEY` contact at the bottom, vertical order `1 2 4 5 6 7 8 9 3`), bracketed `+16V.D.C. LAMP B+ DRIVER BOARD`. The four BLU wires fan out to eight 2P4 contacts through the bundle line; the sheet does not show which BLU wire reaches which 2P4 pin. (Label printed `+16V.D.C.` even though the board-side net is labelled `+18V.D.C.`.)
- Pins 9-12 (BLK x4) go into a bundle line that ends at `2P6` (eight contacts without pin numbers and a `KEY` contact at the top). No label or bracket text is printed for 2P6.
- Pins 1-4 (BLK x4) go into a bundle line that ends at `2P10` (eight contacts without pin numbers and a `KEY` contact at the bottom). No label or bracket text is printed for 2P10.

### 3P6 (+5 V, +12 V, ground to the driver board and CPU board)

3P6 harness-side pins and wire colours, vertical order as printed: 4 `GRY`, 10 `GRY`, 9 `GRY`, 8 `GRY`, 7 `GRY`, 3 `N.C.`, 6 `GRY-WHT`, 2 (stub line, unlabelled), 14 `BLK`, 13 `BLK`, 12 `BLK`, 11 `BLK`, 15 `N.C.`.

- GRY x5 (pins 4, 10, 9, 8, 7) join a bundle line that fans out to `2P8` pins 2, 3, 4 (bracket `+5V.D.C. DRIVER BOARD`) and `1P2` pins 4, 5, 6 (bracket `+5V.D.C.`, part of the `CPU BOARD` bracket). `2P8` pin 1 has a short free stub drawn only on the harness side and nothing connected.
- GRY-WHT (pin 6) runs right, turns down and then right (drawn as one continuous line, no junctions) to `1P2` pin 9 (label `+12V.D.C. UNREG.`). 3P6 pin 6 board-side is on the +12 V bus.
- BLK x4 (pins 14, 13, 12, 11) join a bundle line that fans out to `2P8` pins 6, 7, 8, 9 (bracket `GROUND DRIVER BOARD`) and `1P2` pins 1, 2, 3 (bracket `GROUND`). Board side: pins 14, 13, 12, 11, 15 are on a ground bus.
- Pin 3 `N.C.`, pin 15 `N.C.`, pin 2 an unlabelled stub.
- `1P2` pins in vertical order: 1, 2, 3 (`GROUND`), 4, 5, 6 (`+5V.D.C.`), 7 (`KEY`), 9 (`+12V.D.C. UNREG.`); whole connector bracketed `CPU BOARD`. There is no pin 8.

### 3P7 and the K1 SPECIAL RELAY

3P7 pins as printed (harness side): 1 label `DRIVER BOARD SOL.11 (Q35)` with wire colour `BRN-ORN`; 2 `N.C.`; 3 wire colour `RED` (routed down and to the right, long horizontal at the bottom, joining the same vertical as the `RED` wire from 3P3 pin 8, i.e. the +38 solenoid supply).

Board side:
- 3P7 pin 1 -> the top end of the K1 coil; pin 3 -> the bottom end of the K1 coil. Coil symbol labelled `K1` / `SPECIAL` / `RELAY` (printed `KI SPECIAL RELAY`).
- A diode is drawn across the coil (junction dots at both ends): the triangle points downward, the bar is at its lower end, i.e. its cathode end is at the 3P7 pin 3 end and its anode end at the 3P7 pin 1 end.
- 3P7 pin 2: board-side arrow with a short stub line, nothing connected.

K1 contact (switch drawn at 3P9 pin 1): drawn as a blade pivoting at the left terminal circle (the 3P9-1 side) and running to the right underneath the right terminal circle, with its tip extending slightly beyond it. A vertical dashed line (the mechanical link) runs from the blade tip down to the K1 coil. At the scan's resolution the blade lies against the underside of the right terminal; whether a hairline gap is printed there cannot be read reliably (one reading of the page saw a gap, the curator's zoom shows the blade at the terminal). The sheet prints no NO/NC legend. As drawn, the coil pulls the blade down, away from the right terminal, which is a contact that opens when the relay is energized. 3P9 pin 2 has no contact in series; its fuse `F6 20A` is a plain fuse symbol.

### 3P8 (general illumination, 6.3 V.A.C. not labelled on this sheet)

No `6.3` voltage label or `V.A.C.` text appears anywhere on this sheet except the `18.7 V.A.C. C.T.` text on 10P1. The 3P8 section carries no printed voltage; I describe the routing as drawn only.

3P8 board-side header pins in vertical order: 6, 7, 8, 9, 1, 2, 3, 4, 5 (bottom, `KEY`). Pins 6, 7, 8, 9 are tied to one vertical (junction dots on 6, 7, 8; pin 9 line ends on it) that connects up to the `F6 20A` line. Pins 1, 2, 3, 4 are tied to another vertical (junction dots on 1, 2, 3; pin 4 line joins it) that connects up to the K1 contact line. Pin 5 is the `KEY` position (a dash stub on the harness side).

Harness-side wire labels in vertical order (slots 1-9, each label printed just above its wire): `WHT-YEL`, `WHT`, `WHT-YEL`, `WHT-YEL`, `YEL`, `VIO`, `YEL`, `YEL`, then a blank stub for the ninth slot. Reading each label with the board-side pin number in the same row: pin 6 `WHT-YEL`; pin 7 `WHT`; pin 8 `WHT-YEL`; pin 9 `WHT-YEL`; pin 1 `YEL`; pin 2 `VIO`; pin 3 `YEL`; pin 4 `YEL`; pin 5 stub (unlabelled). [uncertain: the labels sit between two adjacent wires and could be assigned to the wire above or below; I assigned each label to the wire immediately beneath it.]

Harness routing as drawn:

- Wire `WHT` (pin 7) runs straight to the first `8J8` contact (8J8 pin 4).
- Wires `WHT-YEL` (pins 6, 8, 9) turn into a bold bundle line (x about 3650 px) running down the sheet; from a junction on this bundle a branch goes to the third 8J8 contact (8J8 pin 5), and the bundle continues down to `9P1` pins 2 and 5.
- Wires `YEL` (pins 1, 3, 4) turn into a second bold bundle line (x about 3590 px), as does the `VIO` wire; from a junction on it a branch goes to the fifth 8J8 contact (8J8 pin 2); this bundle continues down to `9P1` pins 1 and 4. The `VIO` wire (pin 2) also runs right and up directly to the second 8J8 contact (8J8 pin 1), as drawn. [uncertain: whether the VIO wire is the one that reaches 8J8 pin 1 or the junction branch of a YEL wire does; the sheet shows both a direct line from the VIO row to 8J8 pin 1 and a diagonal from the VIO row into the second bundle.]
- 8J8 pin 3 and 8J8 pin 6 have vertical lines leaving to the left that run down to `7P1` pins 1 and 2 respectively (8J8-3 -> 7P1-1, 8J8-6 -> 7P1-2).

### 8J8 / 8P8 / 8P5 / 7P1 / 9P1 (the General Illumination loads)

- `8J8` pins in vertical order: 4, 1, 5, 2, 3, 6 (six contacts); `8P8` pins in the same order (4, 1, 5, 2, 3, 6), drawn facing it.
- `8P8` pins 4 and 1 go straight across to `8P5` pins 2 and 1 (bracket label `LOWER PLAYFIELD`).
- `8P8` pins 5, 2, 3, 6 go to a drawing of a single lamp (a circle with a `D`-like filament) with the label `UPPER PLAYFIELD`: pins 5 and 6 are joined (via a rectangle loop) to the top node of the lamp symbol, and pins 2 and 3 are joined to the bottom node of the lamp symbol (junction dots at the two lamp nodes).
- `7P1` (pins 2 and 1, label `CABINET`): pin 2 fed from 8J8 pin 6, pin 1 fed from 8J8 pin 3 (see above).
- `9P1` (pins in vertical order 2, 5, 1, 4; label `INSERT BOARD`): pins 2 and 5 are fed from the WHT-YEL bundle; pins 1 and 4 are fed from the YEL/VIO bundle.

Summary of the GI routing as drawn: the K1 relay contact (3P9 pin 1) feeds the four 3P8 pins 1-4 (harness wires YEL, VIO, YEL, YEL), while the F6 20A fuse (3P9 pin 2) feeds the four 3P8 pins 6-9 (WHT-YEL, WHT, WHT-YEL, WHT-YEL). The lower-playfield load (8P5), the upper-playfield load (8P8 pins 5/6 and 2/3), the cabinet load (7P1) and the insert-board load (9P1) are all reached from these eight wires and the two bundle lines; the sheet does not label which load is on the switched side.

## Observations

1. The designator `F6` is printed twice (7ASB at 3P1 pin 11, and 20A at 3P9 pin 2); the board therefore shows six fuse designators F1-F6 for seven fuse symbols.
2. 2P4 is labelled `+16V.D.C. LAMP B+ DRIVER BOARD` while the net feeding it from 3P4 pins 5-8 is the `+18V.D.C.` line from F3 (printed inconsistently).
3. 3P4 pins 5-8 (4 wires) feed 2P4's eight contacts; 3P4 pins 9-12 (4 wires) feed the eight-contact 2P6; 3P4 pins 1-4 (4 wires) feed the eight-contact 2P10. 3P6's five GRY wires feed 2P8 pins 2, 3, 4 and 1P2 pins 4, 5, 6 (six contacts) and its four BLK wires feed 2P8 pins 6, 7, 8, 9 and 1P2 pins 1, 2, 3 (seven contacts); the sheet shows the bundle lines but not individual wire-to-pin assignments.
4. The `K1 SPECIAL RELAY` coil is fed on its pin-3 end from the +38 Solenoid B+ net (via the RED wire from 3P3 pin 8 to 3P7 pin 3) and switched to ground at the pin-1 end by `DRIVER BOARD SOL.11 (Q35)`, matching Table 4 row 11 (`Special Relay`, `BRN-ORN`, `2P9-1, 10P3-11`, transistor `Q35` / `Q17`). [3P7 on this sheet is the board connector; the Table 4 connection list names 2P9-1 and 10P3-11.]
5. The contact on 3P9 pin 1 is drawn with the blade under the right terminal and the dashed link running down from the blade tip to the coil, so energizing K1 moves the blade away from that terminal. The sheet does not label the contact NO or NC.
6. The note in the solenoid-locations footnote says the special relay is located on the Power Supply Board (games with transformer in cabinet) or in backbox (games with transformer in backbox); this sheet places the relay inside the Power Supply Board rectangle (consistent with the `D 8345 board (equipped with relay)` statement in the booklet).

## Uncertain readings (this file)

- Assignment of 3P8 harness colour labels to individual slots (see 3P8 section).
- Which wires are in which bundle at the 3P8 outputs, and how the VIO wire reaches 8J8 pin 1.
- Exact wire-to-pin assignment within the 2P4, 2P6, 2P8, 1P2 and 2P10 bundles.
- 3P3 pin 8 RED continuing to 3P7 pin 3: the long RED line is drawn as one continuous line from 3P3 pin 8 down the sheet, then left along the bottom to 3P7 pin 3 RED; no junction dot interrupts it.
- The ground bus of 3P6 pins 14-11 and 15: pin 15 is drawn as a board-side arrow on the same ground net; its harness side is `N.C.`
